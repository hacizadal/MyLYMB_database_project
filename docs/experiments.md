# Experiments

All experiments are defined in `experiments.py` (`CHANGES`, `ALGORITHMS`); the matrix run by `sweep.sh`
is the Cartesian product of both. List them with `python run_alter.py --list`.

## Changes

| Name | Table | ALTER specification | Purpose |
|---|---|---|---|
| change-type | user_table | `MODIFY COLUMN birth_date DATETIME NOT NULL` | Storage format changes (DATE is 3 bytes, DATETIME is 5 bytes + fractional part). |
| add-index | user_table | `ADD INDEX idx_username (username)` | Secondary index; `username` is unique per row in the generated data. |
| widen-column-60 | user_table | `MODIFY COLUMN email_address VARCHAR(60) NOT NULL` | VARCHAR(30) to (60), utf8mb4: 120 to 240 bytes, length prefix stays 1 byte. |
| widen-column-100 | user_table | `MODIFY COLUMN email_address VARCHAR(100) NOT NULL` | 120 to 400 bytes: length prefix grows from 1 to 2 bytes. |
| add-fk | orders | `ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id)` | `foreign_key_checks` ON (MariaDB default). |
| add-fk-fkchecks-off | orders | same | Same ALTER, but the ALTER's connection first runs `SET SESSION foreign_key_checks=0`. |

The 255-byte boundary is the reason for two widen-column variants. **The audit's hypothesis (30 to 60 is metadata-only, 30 to 100 needs a rebuild) is a hypothesis
for MariaDB 11.4. On the sandbox server (10.11.14) it was NOT confirmed: both variants completed in about
0.04-0.05 s on 200,000 rows, including with `ALGORITHM=INSTANT`. A separate one-off check on that server
showed `first_name` VARCHAR(50) to VARCHAR(70) (200 to 280 bytes) refused with `ALGORITHM=INSTANT`, so
the rule is not simply "crossing 255 bytes"; the mechanism was not investigated. Requires runtime
verification on 11.4.**

## Algorithms (requested clause)

| Name | Clause appended to the ALTER | Meaning |
|---|---|---|
| default | none | Server picks algorithm and lock. Reference for "what a developer gets by default". |
| blocking | `ALGORITHM=COPY, LOCK=EXCLUSIVE` | Explicit offline baseline. |
| copy | `ALGORITHM=COPY, LOCK=NONE` | Asks for a table copy without locking. MariaDB is expected to refuse it (see below). |
| copy-shared | `ALGORITHM=COPY, LOCK=SHARED` | Table copy; concurrent reads allowed, writes wait. |
| inplace | `ALGORITHM=INPLACE, LOCK=NONE` | Fails if the operation cannot be done in place without locking. |
| nocopy | `ALGORITHM=NOCOPY, LOCK=NONE` | Fails if the table would have to be rebuilt. |
| instant | `ALGORITHM=INSTANT` | Fails unless the change is metadata-only. |

An explicit `ALGORITHM=` / `LOCK=` is a demand: if the server cannot honour it, the statement fails instead of
falling back to something slower. This is what makes unsupported combinations observable.

## Session configuration is not an algorithm

`foreign_key_checks` is a session variable. `add-fk-fkchecks-off` therefore is a separate **change**
(different session configuration), combined with the same algorithms as any other change. It is recorded in the
`session_config` column. With checks OFF, MariaDB does not re-validate existing rows against the parent
table, so the constraint may be added over orphan rows; the generated dataset has none.

## Observed on the sandbox server (not MariaDB 11.4)

During development, single `ALTER` statements were run on **MariaDB 10.11.14** (the only version installable
in the development sandbox) against 50,000 rows. These observations validate the tooling; they must be
re-checked on 11.4.

| Change | Requested | Outcome | Message (abridged) |
|---|---|---|---|
| change-type | instant / nocopy / inplace | refused (1846) | "Cannot change column type. Try ALGORITHM=COPY" |
| change-type | copy (LOCK=NONE) | refused (1846) | "COPY algorithm requires a lock. Try LOCK=SHARED" |
| add-fk | inplace, checks ON | refused (1846) | "Adding foreign keys needs foreign_key_checks=OFF" |
| add-fk-fkchecks-off | inplace | success | - |

The full-matrix run is described in the README (Results) and stored in `results/validation_sandbox_mariadb10.11/`.
