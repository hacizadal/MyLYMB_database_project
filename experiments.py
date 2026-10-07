"""Experiment registry: which schema changes and which ALTER algorithms exist.

Adding an experiment = adding one entry to CHANGES. Nothing else needs to change.

Two concepts are kept strictly separate:

* ALGORITHM / LOCK clause  -> part of the ALTER statement itself (ALGORITHMS below).
* SESSION configuration    -> `SET SESSION ...` statements run on the ALTER's
                              connection *before* the ALTER (Change.session).
                              `foreign_key_checks=0` is a session setting, not an algorithm.

NOTE: SQL below is built only from these constants, never from user input.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Change:
    family: str            # experiment family (change-type, add-index, widen-column, add-fk)
    table: str             # table the ALTER targets
    alter: str             # ALTER TABLE alter_specification (without algorithm/lock)
    description: str
    session: tuple = ()    # SET SESSION statements executed before the ALTER
    profile: str = "user_table"   # which table the concurrent workload writes to
    needs_orders: bool = False    # does the experiment need the `orders` table populated?


CHANGES = {
    "change-type": Change(
        family="change-type", table="user_table",
        alter="MODIFY COLUMN birth_date DATETIME NOT NULL",
        description="DATE -> DATETIME (storage format changes)."),
    "add-index": Change(
        family="add-index", table="user_table",
        alter="ADD INDEX idx_username (username)",
        description="Add a secondary index on a near-unique VARCHAR column."),
    "widen-column-60": Change(
        family="widen-column", table="user_table",
        alter="MODIFY COLUMN email_address VARCHAR(60) NOT NULL",
        description="VARCHAR(30) -> VARCHAR(60). utf8mb4: 120 -> 240 bytes, still <= 255 "
                    "(1 length byte before and after)."),
    "widen-column-100": Change(
        family="widen-column", table="user_table",
        alter="MODIFY COLUMN email_address VARCHAR(100) NOT NULL",
        description="VARCHAR(30) -> VARCHAR(100). utf8mb4: 120 -> 400 bytes, crosses 255 "
                    "(length prefix grows from 1 to 2 bytes)."),
    "add-fk": Change(
        family="add-fk", table="orders",
        alter="ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id)",
        description="Add a foreign key orders.user_id -> user_table.id, foreign_key_checks ON "
                    "(MariaDB default).",
        profile="orders", needs_orders=True),
    "add-fk-fkchecks-off": Change(
        family="add-fk", table="orders",
        alter="ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id)",
        description="Same foreign key, but with SET SESSION foreign_key_checks=0 on the ALTER's "
                    "connection (existing rows are not re-validated).",
        session=("SET SESSION foreign_key_checks=0",),
        profile="orders", needs_orders=True),
}

# name -> (clause appended to the ALTER, description)
ALGORITHMS = {
    "default":  ("", "No clause: the server picks algorithm and lock level itself."),
    "blocking": ("ALGORITHM=COPY, LOCK=EXCLUSIVE",
                 "Explicit offline baseline: table copy, no reads or writes allowed."),
    "copy":     ("ALGORITHM=COPY, LOCK=NONE",
                 "Ask for a table copy while staying online (MariaDB is expected to refuse: error 1846)."),
    "copy-shared": ("ALGORITHM=COPY, LOCK=SHARED",
                    "Table copy allowing concurrent reads only; writes wait."),
    "inplace":  ("ALGORITHM=INPLACE, LOCK=NONE", "In-place InnoDB DDL, concurrent DML allowed."),
    "nocopy":   ("ALGORITHM=NOCOPY, LOCK=NONE",
                 "Only if the table is not rebuilt; otherwise the statement fails."),
    "instant":  ("ALGORITHM=INSTANT", "Metadata-only change; otherwise the statement fails."),
}


def build_alter_sql(change_name, algorithm_name):
    change = CHANGES[change_name]
    clause = ALGORITHMS[algorithm_name][0]
    sql = f"ALTER TABLE {change.table} {change.alter}"
    return f"{sql}, {clause}" if clause else sql
