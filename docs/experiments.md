# Experiments

All experiments are defined in `experiments.py` (`CHANGES`, `ALGORITHMS`); the matrix run by `sweep.sh`
is the Cartesian product of both. List them with `python run_alter.py --list`.

## Changes

| Name | Table | ALTER specification | Purpose |
|---|---|---|---|
| change-type | user_table | `MODIFY COLUMN birth_date DATETIME NOT NULL` | Storage format changes (DATE is 3 bytes, DATETIME is 5 bytes + fractional part). |
| add-index | user_table | `ADD INDEX idx_username (username)` | Secondary index; `username` is unique per row in the generated data. |
| widen-column-60 | user_table | `MODIFY COLUMN email_address VARCHAR(60) NOT NULL` | VARCHAR(30) to (60), utf8mb4: 120 to 240 bytes, length prefix stays 1 byte. |
| widen-column-100 | user_table | `MODIFY COLUMN email_address VARCHAR(100) NOT NULL` | 120 to 400 bytes: crosses 255, but the old maximum is ≤ 127 bytes. |
| widen-column-rebuild | user_table | `MODIFY COLUMN first_name VARCHAR(100) NOT NULL` | 200 to 400 bytes: old maximum between 128 and 255 bytes, new one above 255. |
| add-fk | orders | `ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id)` | `foreign_key_checks` ON (MariaDB default). |
| add-fk-fkchecks-off | orders | same | Same ALTER, but the ALTER's connection first runs `SET SESSION foreign_key_checks=0`. |

**Why three widen-column variants.** The original hypothesis was "30 → 60 is metadata-only, 30 → 100 needs a
rebuild because it crosses 255 bytes". The 10.11 validation run refuted it: both were instant. The InnoDB rule
(COMPACT/DYNAMIC row formats, MariaDB ≥ 10.4.3) explains why. Each stored VARCHAR value has a 1-byte length prefix
if it is shorter than 128 bytes or the column maximum is ≤ 255 bytes, and a 2-byte prefix otherwise. So:

* old maximum ≤ 127 bytes (our `email_address`, 120 bytes): no stored value can reach 128 bytes, every prefix stays
  1 byte, and **any** widening is INSTANT, even past 255;
* old maximum 128 to 255 bytes (our `first_name`, 200 bytes) and new maximum > 255: existing values of 128+ bytes
  would need a 2-byte prefix, so **INSTANT is refused** and the table must be rebuilt (`widen-column-rebuild`).
  An earlier one-off check on 10.11 (`first_name` 50 → 70 characters, 200 → 280 bytes, INSTANT refused) fits this rule.

Source: [InnoDB online DDL operations with ALGORITHM=INSTANT](https://mariadb.com/kb/en/innodb-online-ddl-operations-with-the-instant-alter-algorithm/).

## Algorithms (requested clause)

| Name | Clause appended to the ALTER | Meaning |
|---|---|---|
| default | none | Server picks algorithm and lock. Reference for "what a developer gets by default". |
| blocking | `ALGORITHM=COPY, LOCK=EXCLUSIVE` | Explicit offline baseline. |
| copy | `ALGORITHM=COPY, LOCK=NONE` | Table copy while writes continue, via the online change buffer. Exists from MariaDB 11.2; refused on 10.11 (see below). |
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

## Observed on MariaDB 11.4.9 (full matrix, 1,000,000 rows)

`ALGORITHM=COPY, LOCK=NONE` succeeded for all 7 changes, including add-fk with `foreign_key_checks=1`. The refusals left
on 11.4 are the ones a copy-free algorithm cannot do: change-type and widen-column-rebuild (`Cannot change column type`),
add-fk with checks ON for INPLACE/NOCOPY, and INSTANT for anything that adds an index. Full tables: README §14.2;
data: `results/sandbox_mariadb11.4_1M/`.
