"""Unit tests: no running MariaDB server required."""
import csv
import random
import threading
from types import SimpleNamespace

import pymysql
import pytest

from workload import CsvSink, FIELDS, OrdersProfile, Stats, UserProfile, Worker


class FakeCursor:
    def __init__(self, error=None):
        self.error = error
        self.lastrowid = 42
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def execute(self, sql, params):
        self.calls.append((sql, params))
        if self.error:
            raise self.error
        return 1


class FakeConnection:
    def __init__(self, error=None):
        self.cur = FakeCursor(error)
        self.closed = False

    def cursor(self):
        return self.cur

    def close(self):
        self.closed = True


@pytest.mark.parametrize("profile,table", [
    (UserProfile, "user_table"),
    (OrdersProfile, "orders"),
])
def test_profile_statements_target_correct_table(profile, table):
    p = profile(random.Random(1), 0, 100)
    insert_sql, _ = p.insert()
    update_sql, _ = p.update(42)
    delete_sql, _ = p.delete(42)
    assert insert_sql.startswith(f"INSERT INTO {table} ")
    assert update_sql.startswith(f"UPDATE {table} ")
    assert delete_sql.startswith(f"DELETE FROM {table} ")


def make_worker(tmp_path, error=None):
    sink = CsvSink(tmp_path / "workload.csv")
    args = SimpleNamespace(seed=1, profile="user_table", lock_timeout=1,
                           backlog=0, interval=0)
    worker = Worker(0, args, sink, threading.Event(), Stats(), 100)
    worker.conn = FakeConnection(error)
    return worker, sink


def test_failed_statement_logs_mysql_error_number(tmp_path):
    worker, sink = make_worker(tmp_path, pymysql.err.OperationalError(1205, "Lock wait timeout"))
    ok, last_id = worker._execute("UPDATE", "UPDATE user_table SET country=%s WHERE id=%s",
                                  ("Germany", 42))
    sink.close()
    with open(tmp_path / "workload.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert set(rows[0]) == set(FIELDS)
    assert not ok and last_id is None
    assert rows[0]["operation"] == "UPDATE"
    assert rows[0]["status"] == "error"
    assert rows[0]["errno"] == "1205"
    assert "Lock wait timeout" in rows[0]["error"]
    assert worker.stats.data["UPDATE"]["err"] == 1


def test_successful_statement_logs_row_count(tmp_path):
    worker, sink = make_worker(tmp_path)
    ok, last_id = worker._execute("INSERT", *worker.profile.insert())
    sink.close()
    with open(tmp_path / "workload.csv", newline="", encoding="utf-8") as f:
        row = next(csv.DictReader(f))
    assert ok and last_id == 42
    assert row["status"] == "success"
    assert row["rows_affected"] == "1"
    assert row["errno"] == ""


def test_connection_loss_is_logged_and_reconnect_requested(tmp_path):
    worker, sink = make_worker(tmp_path, pymysql.err.OperationalError(2006, "Server gone away"))
    old_conn = worker.conn
    ok, _ = worker._execute("DELETE", "DELETE FROM user_table WHERE id=%s", (42,))
    sink.close()
    assert not ok
    assert old_conn.closed
    assert worker.conn is None
    with open(tmp_path / "workload.csv", newline="", encoding="utf-8") as f:
        assert next(csv.DictReader(f))["errno"] == "2006"
