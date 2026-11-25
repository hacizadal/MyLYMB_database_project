"""Isolated MariaDB replication benchmark; never connects to the original lab."""
import argparse
import csv
import hashlib
import os
import random
import statistics
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import pymysql

CONFIGS = {'instant': 'ALGORITHM=INSTANT, LOCK=NONE',
           'online-copy': 'ALGORITHM=COPY, LOCK=NONE',
           'blocking-copy': 'ALGORITHM=COPY, LOCK=EXCLUSIVE'}


def connect(port):
    return pymysql.connect(host='127.0.0.1', port=port, user='root',
                           password=os.environ['REPL_LAB_PASSWORD'], autocommit=True,
                           connect_timeout=5, read_timeout=150, write_timeout=150)


def query(conn, sql, args=None):
    with conn.cursor() as cur:
        cur.execute(sql, args)
        return cur.fetchall()


def status(conn):
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute('SHOW SLAVE STATUS')
        s = cur.fetchone()
    if not s or s['Slave_IO_Running'] != 'Yes' or s['Slave_SQL_Running'] != 'Yes':
        raise RuntimeError(f'Replication unhealthy: {s}')
    return s


def catch_up(primary, replica):
    file, pos, *_ = query(primary, 'SHOW MASTER STATUS')[0]
    result = query(replica, 'SELECT MASTER_POS_WAIT(%s,%s,120)', (file, pos))[0][0]
    if result is None or result < 0:
        raise RuntimeError('Replica did not catch up')
    status(replica)


def setup(p, r):
    # Account created before the starting position; all subsequent DDL/DML is replicated.
    secret = os.environ['REPL_LAB_PASSWORD']
    query(p, "CREATE USER 'lab_repl'@'%%' IDENTIFIED BY %s", (secret,))
    query(p, "GRANT REPLICATION SLAVE ON *.* TO 'lab_repl'@'%'")
    file, pos, *_ = query(p, 'SHOW MASTER STATUS')[0]
    query(r, "CHANGE MASTER TO MASTER_HOST='primary', MASTER_USER='lab_repl', MASTER_PASSWORD=%s, MASTER_LOG_FILE=%s, MASTER_LOG_POS=%s", (secret, file, pos))
    query(r, 'START SLAVE')
    deadline = time.monotonic() + 60
    while True:
        try:
            status(r)
            break
        except RuntimeError:
            if time.monotonic() > deadline:
                raise
            time.sleep(.25)
    query(p, 'CREATE DATABASE repl_lab')
    catch_up(p, r)


def seed(p, r, rows):
    query(p, 'DROP TABLE IF EXISTS repl_lab.items, repl_lab.heartbeat')
    query(p, 'CREATE TABLE repl_lab.items (id INT PRIMARY KEY, email VARCHAR(30) NOT NULL, counter INT NOT NULL DEFAULT 0) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4')
    query(p, 'CREATE TABLE repl_lab.heartbeat (id INT PRIMARY KEY, seq BIGINT NOT NULL, sent DOUBLE NOT NULL) ENGINE=InnoDB')
    query(p, 'INSERT INTO repl_lab.heartbeat VALUES (1,0,%s)', (time.time(),))
    with p.cursor() as cur:
        for start in range(1, rows+1, 1000):
            cur.executemany('INSERT INTO repl_lab.items (id,email) VALUES (%s,%s)', [(i, f'u{i}@example.test') for i in range(start,min(start+1000,rows+1))])
    catch_up(p, r)


def digest(conn):
    h = hashlib.sha256()
    count = 0
    with conn.cursor(pymysql.cursors.SSCursor) as cur:
        cur.execute('SELECT id,email,counter FROM repl_lab.items ORDER BY id')
        for row in cur:
            h.update(repr(row).encode()+b'\n')
            count += 1
    schema = query(conn, 'SHOW CREATE TABLE repl_lab.items')[0][1]
    heartbeat = query(conn, 'SELECT * FROM repl_lab.heartbeat')
    return count, h.hexdigest(), schema, heartbeat


def write_csv(path, records):
    if records:
        with path.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=list(records[0]))
            w.writeheader(); w.writerows(records)


def run(p, r, rows, name, repeat, out):
    seed(p,r,rows)
    stop = threading.Event(); errors = []; writes = []; samples = []
    start = time.monotonic(); markers = {}
    def writer():
        try:
            with connect(13306) as c:
                seq = 0
                while not stop.is_set():
                    t = time.monotonic(); seq += 1
                    c.begin()
                    query(c,'UPDATE repl_lab.items SET counter=counter+1 WHERE id=%s', ((seq-1)%rows+1,))
                    query(c,'UPDATE repl_lab.heartbeat SET seq=%s,sent=%s WHERE id=1',(seq,time.time()))
                    c.commit()
                    writes.append(dict(start_s=t-start,end_s=time.monotonic()-start,latency_ms=(time.monotonic()-t)*1000,seq=seq))
                    stop.wait(.02)
        except Exception as e:
            errors.append(str(e)); stop.set()
    def sampler():
        try:
            with connect(13306) as a, connect(13307) as b:
                while not stop.is_set():
                    # Read replica first; primary read follows, so gap is an upper-biased snapshot.
                    rs, sent = query(b,'SELECT seq,sent FROM repl_lab.heartbeat WHERE id=1')[0]
                    ps = query(a,'SELECT seq FROM repl_lab.heartbeat WHERE id=1')[0][0]
                    s = status(b)
                    samples.append(dict(elapsed_s=time.monotonic()-start,primary_seq=ps,replica_seq=rs,sequence_gap=ps-rs,heartbeat_age_ms=max(0,(time.time()-sent)*1000),seconds_behind_master=s['Seconds_Behind_Master'],io_running=s['Slave_IO_Running'],sql_running=s['Slave_SQL_Running'],last_sql_errno=s['Last_SQL_Errno'],last_io_errno=s['Last_IO_Errno']))
                    stop.wait(.1)
        except Exception as e:
            errors.append(str(e)); stop.set()
    threads = [threading.Thread(target=writer),threading.Thread(target=sampler)]
    for t in threads: t.start()
    try:
        time.sleep(3)
        if errors: raise RuntimeError(errors)
        markers['alter_start_s']=time.monotonic()-start
        query(p, 'ALTER TABLE repl_lab.items MODIFY email VARCHAR(60) NOT NULL, '+CONFIGS[name])
        markers['alter_end_s']=time.monotonic()-start
        time.sleep(5)
    finally:
        stop.set()
        for t in threads: t.join()
        write_csv(out/f'{name}_{repeat}_writes.csv',writes)
        write_csv(out/f'{name}_{repeat}_lag.csv',samples)
    if errors: raise RuntimeError(errors)
    drain_start=time.monotonic(); catch_up(p,r); drain=time.monotonic()-drain_start
    a,b=digest(p),digest(r)
    consistent=a==b and a[0]==rows
    during=[w['latency_ms'] for w in writes if w['start_s']<=markers['alter_end_s'] and w['end_s']>=markers['alter_start_s']]
    after=[s for s in samples if s['elapsed_s']>=markers['alter_end_s'] and s['sequence_gap']==0]
    return dict(configuration=name,repeat=repeat,rows=rows,**markers,alter_s=markers['alter_end_s']-markers['alter_start_s'],max_sequence_gap=max(s['sequence_gap'] for s in samples),max_heartbeat_age_ms=max(s['heartbeat_age_ms'] for s in samples),first_zero_gap_after_alter_s=after[0]['elapsed_s']-markers['alter_end_s'] if after else '',drain_wait_s=drain,overlap_writes=len(during),max_overlap_write_ms=max(during) if during else '',primary_count=a[0],replica_count=b[0],primary_sha256=a[1],replica_sha256=b[1],consistent=consistent)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--rows',type=int,default=100000); parser.add_argument('--repeats',type=int,default=3); args=parser.parse_args()
    if args.rows<1 or args.repeats<1: parser.error('positive rows and repeats required')
    out=Path('results')/('replication_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')); out.mkdir(parents=True,exist_ok=False)
    records=[]
    with connect(13306) as p, connect(13307) as r:
        setup(p,r)
        order=[(n,i) for i in range(1,args.repeats+1) for n in CONFIGS]; random.Random(42).shuffle(order)
        for n,i in order:
            print(f'{n} repeat {i}',flush=True)
            record=run(p,r,args.rows,n,i,out); records.append(record); write_csv(out/'replication_results.csv',records)
            print(record,flush=True)
            if not record['consistent']: raise RuntimeError('Consistency check failed')
    summary=[]
    for n in CONFIGS:
        group=[x for x in records if x['configuration']==n]
        summary.append(dict(configuration=n,repeats=len(group),median_alter_s=statistics.median(x['alter_s'] for x in group),max_sequence_gap=max(x['max_sequence_gap'] for x in group),max_heartbeat_age_ms=max(x['max_heartbeat_age_ms'] for x in group),all_consistent=all(x['consistent'] for x in group)))
    write_csv(out/'replication_summary.csv',summary)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots()
    for record in records:
        with (out/f"{record['configuration']}_{record['repeat']}_lag.csv").open() as f: data=list(csv.DictReader(f))
        ax.plot([float(x['elapsed_s'])-record['alter_start_s'] for x in data],[int(x['sequence_gap']) for x in data],label=f"{record['configuration']} r{record['repeat']}")
    ax.set(xlabel='Seconds relative to ALTER start',ylabel='Heartbeat sequence gap'); ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(out/'replication_lag.png',dpi=150); plt.close(fig)
    print(f'Results: {out}')

if __name__=='__main__': main()
