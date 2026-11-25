"""Isolated boundary, metadata-lock and FK probes; never run on production."""
import argparse, csv, time
from pathlib import Path
import pymysql
from common import connect


def run(out):
    rows = []
    c = connect()
    def execute(sql):
        with c.cursor() as cur:
            return cur.execute(sql)
    def probe(case, sql):
        start = time.perf_counter()
        code, message = 0, ''
        try:
            execute(sql)
        except pymysql.MySQLError as e:
            code, message = e.args[0], str(e)
        rows.append(dict(case=case, sql=sql, seconds=time.perf_counter()-start, error_code=code, message=message))
    try:
        for repeat in range(1, 4):
            for n in (30,31,32,50,63,64):
                execute('DROP TABLE IF EXISTS lab_probe')
                execute(f'CREATE TABLE lab_probe (v VARCHAR({n})) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4')
                execute('INSERT INTO lab_probe VALUES (\'sample\')')
                probe(f'boundary_{n}_r{repeat}', 'ALTER TABLE lab_probe MODIFY v VARCHAR(100), ALGORITHM=INSTANT, LOCK=NONE')
            execute('DROP TABLE IF EXISTS lab_probe')
            execute('CREATE TABLE lab_probe (id INT PRIMARY KEY, v VARCHAR(30)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4')
            execute("INSERT INTO lab_probe VALUES (1,'sample')")
            holder = connect(autocommit=False)
            try:
                with holder.cursor() as cur:
                    cur.execute('SELECT * FROM lab_probe')
                execute('SET SESSION lock_wait_timeout=2')
                probe(f'mdl_timeout_r{repeat}', 'ALTER TABLE lab_probe MODIFY v VARCHAR(60), ALGORITHM=INSTANT, LOCK=NONE')
            finally:
                holder.rollback(); holder.close()
            probe(f'mdl_released_r{repeat}', 'ALTER TABLE lab_probe MODIFY v VARCHAR(60), ALGORITHM=INSTANT, LOCK=NONE')
            for checks in (1,0):
                execute('DROP TABLE IF EXISTS lab_child'); execute('DROP TABLE IF EXISTS lab_parent')
                execute('CREATE TABLE lab_parent (id INT PRIMARY KEY) ENGINE=InnoDB')
                execute('CREATE TABLE lab_child (id INT PRIMARY KEY, parent_id INT, INDEX(parent_id)) ENGINE=InnoDB')
                execute('INSERT INTO lab_child VALUES (1,999)')
                execute(f'SET SESSION foreign_key_checks={checks}')
                probe(f'fk_checks_{checks}_r{repeat}', 'ALTER TABLE lab_child ADD FOREIGN KEY(parent_id) REFERENCES lab_parent(id), ALGORITHM=COPY')
                execute('SET SESSION foreign_key_checks=1')
                with c.cursor() as cur:
                    cur.execute('SELECT COUNT(*) FROM lab_child c LEFT JOIN lab_parent p ON c.parent_id=p.id WHERE p.id IS NULL')
                    rows[-1]['message'] += f'; orphan_count_after={cur.fetchone()[0]}'
    finally:
        try:
            execute('SET SESSION foreign_key_checks=1')
            for table in ('lab_child','lab_parent','lab_probe'): execute(f'DROP TABLE IF EXISTS {table}')
        finally:
            c.close()
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open('w', newline='') as f:
                w=csv.DictWriter(f, fieldnames=['case','sql','seconds','error_code','message']); w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,required=True); run(p.parse_args().out)
