"""Isolated boundary, metadata-lock, FK and online-error probes; never run on production."""
import argparse, csv, threading, time
from pathlib import Path
import pymysql
from common import connect

ONLINE_TABLE = 'lab_online'


class Writer(threading.Thread):
    """Inserts one generated value per loop until stopped. Counts inserts and errors."""

    def __init__(self, make_value):
        super().__init__(daemon=True)
        self.make_value = make_value
        self.stop_event = threading.Event()
        self.inserted = 0
        self.errors = 0

    def run(self):
        conn = connect()
        try:
            while not self.stop_event.is_set():
                value = self.make_value(self.inserted + self.errors)
                try:
                    with conn.cursor() as cur:
                        cur.execute(f'INSERT INTO {ONLINE_TABLE} (v) VALUES (%s)', (value,))
                    self.inserted += 1
                except pymysql.MySQLError:
                    self.errors += 1
                self.stop_event.wait(0.002)
        finally:
            conn.close()


def fill_online_table(conn, row_count):
    """Fresh table with unique short values v1, v2, ... (at most 7 characters)."""
    with conn.cursor() as cur:
        cur.execute(f'DROP TABLE IF EXISTS {ONLINE_TABLE}')
        cur.execute(f'CREATE TABLE {ONLINE_TABLE} ('
                    'id INT AUTO_INCREMENT PRIMARY KEY, '
                    'v VARCHAR(30) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4')
        cur.execute(f'INSERT INTO {ONLINE_TABLE} (v) SELECT CONCAT("v", seq) FROM seq_1_to_{int(row_count)}')


def wait_until_running(monitor, connection_id, timeout=5.0):
    """True once the given connection is executing a statement."""
    deadline = time.perf_counter() + timeout
    while time.perf_counter() < deadline:
        with monitor.cursor() as cur:
            cur.execute('SELECT COUNT(*) FROM information_schema.PROCESSLIST WHERE ID = %s AND COMMAND = %s',
                        (connection_id, 'Query'))
            if cur.fetchone()[0]:
                return True
        time.sleep(0.01)
    return False


def inspect_online_table(conn):
    """State after the ALTER: column type, whether the unique index exists, row count."""
    with conn.cursor() as cur:
        cur.execute('SELECT COLUMN_TYPE FROM information_schema.COLUMNS '
                    'WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND COLUMN_NAME = %s',
                    (ONLINE_TABLE, 'v'))
        column_type = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM information_schema.STATISTICS '
                    'WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND INDEX_NAME = %s',
                    (ONLINE_TABLE, 'uq_v'))
        has_unique_index = cur.fetchone()[0] > 0
        cur.execute(f'SELECT COUNT(*) FROM {ONLINE_TABLE}')
        row_count = cur.fetchone()[0]
    return column_type, has_unique_index, row_count


def online_probe(case, sql, make_value, kill_after, row_count):
    """Run one ALTER while a writer inserts rows (or while it is killed); report what happened."""
    setup = connect()
    alter_conn = connect()
    monitor = connect()
    outcome = {'code': 0, 'message': '', 'seconds': 0.0}
    try:
        fill_online_table(setup, row_count)

        def do_alter():
            started = time.perf_counter()
            try:
                with alter_conn.cursor() as cur:
                    cur.execute(sql)
            except pymysql.MySQLError as exc:
                outcome['code'] = exc.args[0] if exc.args and isinstance(exc.args[0], int) else -1
                outcome['message'] = str(exc).replace('\n', ' ')
            outcome['seconds'] = time.perf_counter() - started

        alter_thread = threading.Thread(target=do_alter)
        alter_thread.start()
        running = wait_until_running(monitor, alter_conn.thread_id())
        writer = Writer(make_value) if make_value else None
        if writer and running:
            writer.start()
        stop_seconds = ''
        kill_sent = False
        if kill_after is not None and running:
            time.sleep(kill_after)
            killed_at = time.perf_counter()
            with monitor.cursor() as cur:
                cur.execute(f'KILL {int(alter_conn.thread_id())}')
            kill_sent = True
            alter_thread.join()
            stop_seconds = round(time.perf_counter() - killed_at, 3)
        alter_thread.join()
        if writer and writer.is_alive():
            writer.stop_event.set()
            writer.join(timeout=5)
        column_type, has_unique_index, rows_after = inspect_online_table(monitor)
        details = [f'rows_before={row_count}', f'rows_after={rows_after}', f'column_after={column_type}',
                   f'unique_index_after={has_unique_index}']
        if writer:
            details += [f'writer_inserts={writer.inserted}', f'writer_errors={writer.errors}']
        if kill_after is not None:
            details += [f'kill_sent={kill_sent}', f'seconds_from_kill_to_stop={stop_seconds}']
        message = '; '.join(filter(None, [outcome['message'], *details]))
        return dict(case=case, sql=sql, seconds=outcome['seconds'], error_code=outcome['code'], message=message)
    finally:
        for conn in (setup, alter_conn, monitor):
            conn.close()


ADD_UNIQUE = f'ALTER TABLE {ONLINE_TABLE} ADD UNIQUE INDEX uq_v (v), '
NARROW = f'ALTER TABLE {ONLINE_TABLE} MODIFY v VARCHAR(10) NOT NULL, '
WIDEN_AND_KILL = f'ALTER TABLE {ONLINE_TABLE} MODIFY v VARCHAR(40) NOT NULL, ALGORITHM=COPY, LOCK=NONE'

# (case, SQL, value the writer inserts or None, seconds before KILL or None)
ONLINE_CASES = [
    # Writers insert a duplicate of an existing value while a UNIQUE index is built.
    ('unique_dup_inplace', ADD_UNIQUE + 'ALGORITHM=INPLACE, LOCK=NONE', lambda n: 'v1', None),
    ('unique_dup_copy', ADD_UNIQUE + 'ALGORITHM=COPY, LOCK=NONE', lambda n: 'v1', None),
    # Control: the same ALTER with writers that never conflict.
    ('unique_ok_inplace', ADD_UNIQUE + 'ALGORITHM=INPLACE, LOCK=NONE', lambda n: f'w{n}', None),
    # Writers insert 25 characters while the column is narrowed to 10.
    ('narrow_long_copy', NARROW + 'ALGORITHM=COPY, LOCK=NONE', lambda n: 'x' * 25, None),
    # Control: writers only insert values that still fit.
    ('narrow_short_copy', NARROW + 'ALGORITHM=COPY, LOCK=NONE', lambda n: f'w{n}', None),
    # KILL the running ALTER: how long until it stops, and is the table unchanged?
    ('kill_copy', WIDEN_AND_KILL, None, 0.2),
]


def run(out, online_rows):
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
        for repeat in range(1, 4):
            for case, sql, make_value, kill_after in ONLINE_CASES:
                result = online_probe(case, sql, make_value, kill_after, online_rows)
                result['case'] += f'_r{repeat}'
                rows.append(result)
                print(f"{result['case']}: error_code={result['error_code']} in {result['seconds']:.2f}s", flush=True)
    finally:
        try:
            execute('SET SESSION foreign_key_checks=1')
            for table in ('lab_child','lab_parent','lab_probe', ONLINE_TABLE): execute(f'DROP TABLE IF EXISTS {table}')
        finally:
            c.close()
            out.parent.mkdir(parents=True, exist_ok=True)
            with out.open('w', newline='') as f:
                w=csv.DictWriter(f, fieldnames=['case','sql','seconds','error_code','message']); w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--online-rows', type=int, default=300000,
                   help='rows in the table used by the online-error probes [300000]; use 1000000 for the report')
    args = p.parse_args()
    run(args.out, args.online_rows)
