# Methodology

## Question

How do MariaDB's native online-DDL algorithms (`COPY`, `INPLACE`, `NOCOPY`, `INSTANT`, and the
server default) affect (a) the duration of an `ALTER TABLE` and (b) the latency and error rate of
concurrent INSERT / UPDATE / DELETE statements, without external tools such as pt-online-schema-change?

## One experimental run

Every run starts from the **same** state and is executed by `sweep.sh`:

| Step | Component | What happens |
|---|---|---|
| 1. Reset | `reset_db.py` | `schema.sql` drops and recreates `orders` and `user_table`; `generate_data.py` refills them with the deterministic dataset (`--seed 42`); `ANALYZE TABLE` refreshes statistics. |
| 2. Workload start | `workload.py` (background) | N client connections loop INSERT, UPDATE, DELETE; each statement is timed and logged. `--ready-file` signals that all connections are open. |
| 3. Baseline | `sweep.sh` | The workload runs alone for `--baseline-secs` (default 10 s). |
| 4. ALTER | `run_alter.py` | On its own connection: optional `SET SESSION ...`, then one `ALTER TABLE` with the requested clause. Wall-clock duration, status, error code/message are recorded. A poller samples `information_schema.PROCESSLIST` (ALTER `Progress`, sessions in a `Waiting for ...` state). |
| 5. After | `sweep.sh` | The workload keeps running for `--after-secs` (default 5 s). |
| 6. Stop | `sweep.sh` | SIGTERM to the workload, which flushes its CSV and prints a summary. |
| 7. Next run | | Back to step 1. Nothing from the previous run survives. |

Why reset every time: after a successful change-type, re-running the same change-type does nothing
(the column already has the new type), so the second measurement is meaningless. The reset also
removes index/foreign-key side effects and the rows the workload inserted.

## Workload

* One connection per thread, autocommit, `lock_wait_timeout` and `innodb_lock_wait_timeout` = 10 s
  (configurable) so that statements blocked by the ALTER become measurable errors rather than hanging.
* Each cycle: INSERT one row; UPDATE one random row **that this thread inserted**; once more than
  `--backlog` (50) own rows exist, DELETE the oldest. All UPDATE/DELETE statements use the primary key:
  a full-table scan would make latency depend on table size, not on the ALTER.
* Threads never touch each other's rows or the pre-generated dataset.
* `--profile orders` writes to `orders` (used for add-fk); `--profile user_table` otherwise.
* Timestamps are UTC ISO-8601 with milliseconds, identical to `run_alter.py`, so the two CSVs can be joined.
* A connection lost to a server-side error is reopened; failures are logged with MariaDB's error number.

## Phases and metrics

`analyze_results.py` assigns each workload statement to a phase using its interval
`[start, start + latency]` and the ALTER window `[started_at_utc, ended_at_utc]`:

* **baseline**: finished before the ALTER started.
* **during**: overlaps the ALTER window (a statement started before the ALTER but still blocked by it counts here).
* **after**: started after the ALTER ended.

Per run, operation and phase it reports: count, successes, errors, average, p50, p95, p99, max
(milliseconds). Per change and algorithm it reports ALTER runs, successes, failures, mean, median, min, max
duration (successful runs only) and the first error message. Phases with fewer than 30 statements are
flagged `low_sample`: their percentiles should not be interpreted.

Metadata is stored with each ALTER row: server version, dataset size, exact SQL, session configuration, tag.

## ALTER outcomes

A refused combination (for example error 1846, "ALGORITHM=INSTANT is not supported") is a **result**:
it is stored as `status=failure` with errno and message, with no special-casing. A failure of the
*infrastructure* (cannot connect, reset failed) is not a result: the scripts stop with a non-zero exit code.

## Threats to validity

* Single machine, Docker on a desktop OS; only compare runs made on the same machine and configuration.
* Timings depend on `innodb_buffer_pool_size` and dataset size; the value is written to `sweep_config.txt`.
* The workload is light (one or a few connections, a pause between cycles). It shows interference on
  a few clients, not a saturated server.
* A short ALTER overlaps few workload statements; use a larger `--rows` for meaningful percentiles.
* One repetition per combination by default; use `--repeats 3` or more before drawing conclusions.
* Wall-clock time includes time spent waiting for a metadata lock held by the workload.
