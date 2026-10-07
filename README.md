# MyLYMB Database Project

**Online Schema Change Without External Tools: MariaDB 11.4**

![MariaDB](https://img.shields.io/badge/MariaDB-11.4-003545?logo=mariadb)
![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/11.4%20benchmark-pending-orange)

University project, *Area 8 Tier C: "Online schema change, without external tools"* (MariaDB student database projects, 2026-09).

> **Status.** The tooling is complete and was validated end to end, but on a **MariaDB 10.11** server, not
> on 11.4 (Docker was not available where the tooling was finalized). The 11.4 benchmark itself is
> **pending**: see [Results](#14-results). Nothing below presents 10.11 numbers as 11.4 results.

## Contents

1. [Project Overview](#1-project-overview) · 2. [Research Question](#2-research-question) · 3. [Objectives](#3-objectives) · 4. [Technologies](#4-technologies) · 5. [Architecture](#5-architecture) · 6. [Database Schema](#6-database-schema) · 7. [Experiments](#7-experiments) · 8. [Algorithms](#8-algorithms) · 9. [Workload](#9-workload) · 10. [Methodology](#10-methodology) · 11. [Installation](#11-installation) · 12. [Quick Start](#12-quick-start) · 13. [Running the Benchmark](#13-running-the-benchmark) · 14. [Results](#14-results) · 15. [Findings](#15-findings) · 16. [Limitations](#16-limitations) · 17. [Reproducibility](#17-reproducibility) · 18. [Team](#18-team) · 19. [Project Structure](#19-project-structure) · 20. [Lessons Learned](#20-lessons-learned) · 21. [Conclusion](#21-conclusion)

## 1. Project Overview

Changing a table's structure on a live database is risky: a plain `ALTER TABLE` can rebuild the table and
block every writer for as long as it takes. MariaDB advertises native *online DDL*: several algorithms
(`COPY`, `INPLACE`, `NOCOPY`, `INSTANT`) and lock levels (`LOCK=NONE/SHARED/EXCLUSIVE`) that should let a
table be altered while it is still being written to, without external tools such as `pt-online-schema-change`.

This project builds a small **migration laboratory** to test that claim with measurements: a populated
table, a continuous INSERT/UPDATE/DELETE workload, four families of schema change, each requested with
every algorithm, recording what MariaDB accepts, how long it takes, and what happens to the concurrent writes.

## 2. Research Question

> How do the MariaDB 11.4 online schema-change algorithms affect the execution time of `ALTER TABLE`
> and the latency and error rate of concurrent INSERT, UPDATE and DELETE statements, and which
> algorithm/operation combinations are actually supported?

## 3. Objectives

* **Measure** ALTER duration and per-operation workload latency (p50, p95, p99, max, errors).
* **Compare** a baseline (workload only) with the ALTER window, per algorithm and per change.
* **Observe** which combinations MariaDB refuses, with the exact error code and message.
* **Analyse** the effect of dataset size and of `foreign_key_checks` on adding a foreign key.
* **Understand** *why* an operation is or is not online, using MariaDB's own error messages and `Progress` column.

## 4. Technologies

MariaDB 11.4 (Docker image `mariadb:11.4`, pinned) · Docker Compose · Python 3.10+ with PyMySQL ·
SQL · Bash (`sweep.sh`) · CSV · pandas, numpy, matplotlib (analysis and figures) · ReportLab (PDF report).

## 5. Architecture

```text
Docker (docker-compose.yml)
  └─ MariaDB 11.4 ── schemalab ── user_table, orders
        ▲  reset_db.py = schema.sql + generate_data.py   (identical state before every run)
        │
        ├── workload.py   background INSERT/UPDATE/DELETE, one CSV row per statement
        ├── run_alter.py  one ALTER (+ session config), timed, processlist polled, one CSV row
        │        ▲
        │        └── experiments.py   registry of changes and algorithms
        └── sweep.sh      orchestrates: reset → workload → baseline → ALTER → after → stop, for every combination
                ▼
        results/<sweep_id>/*.csv ── analyze_results.py ──► analysis/*.csv, summary.md, *.png
```

## 6. Database Schema

Defined in [`schema.sql`](schema.sql) (re-runnable: it drops and recreates both tables). Both tables
deliberately start **without** secondary index and **without** foreign key; two experiments add them.

| Table | Columns | Role |
|---|---|---|
| `user_table` | `id` PK, `first_name` VARCHAR(50), `middle_name` VARCHAR(50) NULL, `last_name` VARCHAR(50), `birth_date` DATE, `email_address` VARCHAR(30), `phone_number` VARCHAR(25), `country` VARCHAR(30), `username` VARCHAR(30), `created_at` DATETIME | Target of change-type, add-index, widen-column; parent table of the FK |
| `orders` | `id` PK, `user_id` INT, `order_total` DECIMAL(10,2), `status` VARCHAR(20), `created_at` DATETIME | Child table of add-fk (`user_id` → `user_table.id`) |

Engine InnoDB (required: the online-DDL algorithms are InnoDB features), charset `utf8mb4`
(4 bytes per character, which matters for VARCHAR widening). The `orders` schema is this project's own
design: it was missing from the original repository.

## 7. Experiments

Defined in [`experiments.py`](experiments.py); details in [`docs/experiments.md`](docs/experiments.md).

| Experiment | Table | SQL | Description |
|---|---|---|---|
| `change-type` | user_table | `MODIFY COLUMN birth_date DATETIME NOT NULL` | DATE → DATETIME: the storage format changes. |
| `add-index` | user_table | `ADD INDEX idx_username (username)` | Secondary index on a near-unique column. |
| `widen-column-60` | user_table | `MODIFY COLUMN email_address VARCHAR(60) NOT NULL` | 30 → 60 characters (120 → 240 bytes, stays below 255). |
| `widen-column-100` | user_table | `MODIFY COLUMN email_address VARCHAR(100) NOT NULL` | 30 → 100 characters (120 → 400 bytes, crosses 255). |
| `add-fk` | orders | `ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id)` | `foreign_key_checks` ON (MariaDB default). |
| `add-fk-fkchecks-off` | orders | same | Same ALTER after `SET SESSION foreign_key_checks=0` on the ALTER's connection. |

`foreign_key_checks` is a **session setting, not an algorithm**; that is why add-fk with checks off is a
separate *change* (recorded in the `session_config` CSV column) and not an algorithm called "inplace-checksoff".
Manual SQL versions of the add-fk scenarios are in [`tests/add-fk/`](tests/add-fk/README.md).

## 8. Algorithms

Each change is requested with every algorithm below (`python run_alter.py --list`).

| Name | Clause appended to the ALTER | Meaning |
|---|---|---|
| `default` | *(none)* | The server chooses algorithm and lock level (what a developer gets by default). |
| `blocking` | `ALGORITHM=COPY, LOCK=EXCLUSIVE` | Explicit offline baseline: table copy, no concurrent access. |
| `copy` | `ALGORITHM=COPY, LOCK=NONE` | Table copy *while online*. MariaDB is expected to refuse it. |
| `copy-shared` | `ALGORITHM=COPY, LOCK=SHARED` | Table copy; reads allowed, writes wait. |
| `inplace` | `ALGORITHM=INPLACE, LOCK=NONE` | In-place InnoDB change, concurrent DML allowed. |
| `nocopy` | `ALGORITHM=NOCOPY, LOCK=NONE` | Only if the table is not rebuilt, otherwise an error. |
| `instant` | `ALGORITHM=INSTANT` | Metadata-only change, otherwise an error. |

**Not every combination is supported.** An explicit `ALGORITHM=`/`LOCK=` is a demand: MariaDB fails with
error 1846 instead of silently falling back to something slower. Those failures are recorded as results
(`status=failure`, errno, message), not treated as bugs.

## 9. Workload

[`workload.py`](workload.py) runs `--threads` client connections (autocommit). Each thread loops:

| Step | Statement | Target row |
|---|---|---|
| INSERT | one new row (`user_table`, or `orders` with `--profile orders`) | new |
| UPDATE | `SET country=...` (or `SET status=...`) | random row this thread inserted, **by primary key** |
| DELETE | `DELETE ... WHERE id=?` | oldest row this thread inserted, once more than `--backlog` (50) exist |

Every statement is timed with `time.perf_counter()` and written to CSV: `timestamp_utc` (statement start),
`thread`, `operation`, `latency_ms`, `status`, `errno`, `error`, `rows_affected`. Design choices:
primary-key access (a scan would measure table size, not the ALTER), threads never touch the same rows
or the generated dataset, `lock_wait_timeout` = 10 s so blocked statements end as measurable errors,
automatic reconnection, UTC timestamps identical to `run_alter.py`. It stops on SIGINT/SIGTERM or `--duration`.

## 10. Methodology

Every run (one change × one algorithm) is executed by `sweep.sh` exactly like this:

```text
RESET (schema.sql + generate_data.py, seed 42, ANALYZE)   ← identical start state every time
  → start workload in background, wait until connected
  → baseline phase (workload only, default 10 s)
  → ALTER on its own connection  [processlist polled every 250 ms: Progress, waiting sessions]
  → after phase (default 5 s)
  → stop workload (SIGTERM), save CSVs
  → next run starts from RESET again
```

`analyze_results.py` assigns each workload statement to *baseline* (finished before the ALTER),
*during* (overlaps the ALTER window, including statements blocked by it) or *after*, then computes
count, errors, average, p50, p95, p99 and max per operation and phase. Phases with fewer than 30 statements
are flagged `low_sample`. Full description and threats to validity: [`docs/methodology.md`](docs/methodology.md).

## 11. Installation

Requirements: Docker (Desktop on Windows/macOS), Python 3.10+, Bash (Git Bash or WSL on Windows, for `sweep.sh`).

```bash
git clone <repository-url> && cd MyLYMB_database_project
pip install -r requirements.txt
cp .env.example .env          # optional: every value has a default
docker compose up -d          # MariaDB 11.4, bound to 127.0.0.1 only
docker compose ps             # wait until the container is "healthy"
```

The password defaults to `labpass` (local throw-away container, published on localhost only; never reuse it).
Change it in `.env` **before the first `docker compose up`**: the root password is fixed when the data volume
is created (to apply a new one: `docker compose down -v`, which deletes the lab data). `INNODB_BUFFER_POOL_SIZE`
(default 1G) influences ALTER durations; lower it on machines with little RAM and keep it identical across runs.

## 12. Quick Start

```bash
docker compose up -d && pip install -r requirements.txt
python reset_db.py --rows 100000 --change add-fk      # schema + 100k users + 100k orders
python run_alter.py --list                            # available changes and algorithms
./sweep.sh --rows 100000 --changes "add-index" --algorithms "default inplace" \
           --baseline-secs 3 --after-secs 2           # 2 runs, under a minute
```

The results appear in `results/sweep_<timestamp>/` (raw CSVs) and `.../analysis/` (summary, figures).

## 13. Running the Benchmark

**Full matrix** (6 changes × 7 algorithms = 42 runs per repetition; runtime is dominated by the reset, roughly
15 s per run at 200,000 rows and more at 1,000,000):

```bash
./sweep.sh --rows 1000000 --repeats 3 --threads 2
./sweep.sh --help                                      # all options
python analyze_results.py results/<sweep_id>           # re-run the analysis only
```

**One run by hand** (three terminals or background jobs):

```bash
python reset_db.py --rows 1000000 --change add-index
python workload.py --out results/wl_add-index_inplace.csv --threads 2 &   # terminal 1
python run_alter.py --change add-index --algorithm inplace \
       --out results/alter_results.csv --workload results/wl_add-index_inplace.csv       # terminal 2
kill -TERM %1                                                            # stop the workload
```

Datasets on their own: `python generate_data.py --rows 100000` (or 500000, 1000000; add `--truncate` if the
table is not empty). Generation streams in batches of 5,000 rows; 1,000,000 rows took 32 s with 36 MB of
memory in the validation environment.

## 14. Results

### 14.1 Validated benchmark results (MariaDB 11.4)

**Not run.** *Results will be populated after running the benchmark* (`./sweep.sh --rows 1000000 --repeats 3`)
against the `mariadb:11.4` container. Expected location: `results/sweep_<timestamp>/analysis/`.

### 14.2 Pipeline validation run (sandbox, MariaDB **10.11.14**, not 11.4)

The complete matrix was executed once to prove that the tooling works end to end. Conditions:
MariaDB 10.11.14 (Ubuntu package, no Docker), 256 MB buffer pool, 200,000 rows, 2 workload threads, 4 s baseline,
2 s after, 1 repetition, single machine. Files: [`results/validation_sandbox_mariadb10.11/`](results/validation_sandbox_mariadb10.11/)
(`alter_results.csv`, one workload CSV per run, processlist samples, `analysis/`).
**These are not the project's benchmark results**: other server version, tiny ALTER durations, one repetition.

ALTER duration in seconds (`refused` = MariaDB error 1846, nothing was altered):

| Change | default | blocking | copy | copy-shared | inplace | nocopy | instant |
|---|---|---|---|---|---|---|---|
| change-type | 0.85 | 0.88 | refused | 0.85 | refused | refused | refused |
| add-index | 0.28 | 0.96 | refused | 0.94 | 0.30 | 0.27 | refused |
| widen-column-60 | 0.04 | 0.77 | refused | 0.73 | 0.04 | 0.04 | 0.05 |
| widen-column-100 | 0.05 | 0.77 | refused | 0.96 | 0.04 | 0.04 | 0.05 |
| add-fk | 1.92 | 1.72 | refused | 1.92 | refused | refused | refused |
| add-fk-fkchecks-off | 0.35 | 0.76 | refused | 0.71 | 0.43 | 0.50 | refused |

Maximum latency (ms) of a workload statement overlapping the ALTER, with the number of such statements in
parentheses (successful ALTERs only). With only 1 to 6 statements in most cells, **percentiles are not meaningful here**
(`low_sample` in the CSV); the maximum is shown instead.

| Change | default | blocking | copy | copy-shared | inplace | nocopy | instant |
|---|---|---|---|---|---|---|---|
| change-type | 821 (2) | 863 (2) | - | 829 (2) | - | - | - |
| add-index | 16 (26) | 957 (2) | - | 921 (2) | 25 (27) | 23 (24) | - |
| widen-column-60 | 2 (1) | 730 (2) | - | 708 (4) | 33 (6) | 12 (2) | 30 (2) |
| widen-column-100 | 21 (2) | 723 (2) | - | 933 (6) | 9 (2) | 30 (4) | 36 (3) |
| add-fk | 1915 (4) | 1730 (3) | - | 1885 (2) | - | - | - |
| add-fk-fkchecks-off | 14 (35) | 781 (2) | - | 740 (2) | 12 (42) | 14 (51) | - |

Across this run: 28 ALTERs succeeded and 14 were refused (all with error 1846), and the workload logged **0 errors**
(ALTERs were shorter than the 10 s lock timeout). Figures: `analysis/fig_alter_duration.png`,
`fig_workload_p95.png`, `fig_latency_distribution.png`.

### 14.3 Historical / preliminary results (original repository)

Kept unchanged in [`results/historical/`](results/historical/). **Not comparable with the above and not a
benchmark**: the table was almost empty and the workload never ran at the same time as the ALTERs.

| File | Content |
|---|---|
| `results_alter_preliminary.csv` | 2 ALTERs on a near-empty table (`change-type`: blocking 0.321 s, copy 0.277 s; the second ran on an already-converted column). |
| `workload_baseline_preliminary.csv` | 477 statements over 19 s, no ALTER, 0 errors. Median INSERT 6.88 ms, UPDATE 4.31 ms, DELETE 3.93 ms. |

The historical `copy` row (`ALGORITHM=COPY, LOCK=NONE`, no error) **contradicts** the sandbox run, where that clause was
refused in 6 of 6 experiments (error 1846). Unresolved: to be checked on 11.4.

## 15. Findings

**MariaDB 11.4: pending benchmark execution.**

Indicative observations from the 10.11 validation run only (to be confirmed or refuted on 11.4; one repetition, small samples):

* An explicit algorithm is never silently downgraded: unsupported requests fail with 1846 and a reason
  (e.g. `Cannot change column type`, `COPY algorithm requires a lock`, `Adding foreign keys needs foreign_key_checks=OFF`).
* `ALGORITHM=COPY, LOCK=NONE` was refused for every change; `LOCK=SHARED` was accepted.
* DATE → DATETIME was supported only by table-copy algorithms (and therefore by `default`); `inplace`, `nocopy`, `instant` were refused.
* add-fk with `foreign_key_checks=1`: only copy-style algorithms worked; with `foreign_key_checks=0`, `inplace` and `nocopy` worked.
  `instant` was refused with reason `ADD INDEX`, since a foreign key needs an index on `user_id`.
* Table-copy ALTERs (`default` for change-type and add-fk, `blocking`, `copy-shared`) left concurrent writes waiting roughly as long as the ALTER
  (max workload latency close to ALTER duration). `inplace`/`nocopy`/`instant` runs had workload maxima of about 9-36 ms while the ALTER ran.
* The audit's widen-column hypothesis (30→60 cheap, 30→100 rebuild) was **not** reproduced on 10.11: both completed in about 0.05 s.

## 16. Limitations

* Single machine; Docker (or another environment) adds overhead; compare only runs from the same machine and configuration.
* Light workload: one to a few connections with a pause between cycles. It is not a saturated server.
* Results depend on dataset size, `innodb_buffer_pool_size` and the MariaDB version (11.4 is pinned on purpose).
* A short ALTER overlaps few workload statements, so use large datasets (`--rows 1000000`) and several `--repeats` for percentiles.
* Workload rows are disjoint from the ALTER's scan targets; contention on the *same rows* is not modelled.
* The `orders` foreign key is added with no orphan rows, so `foreign_key_checks=0` does not hide invalid data here.
* `docker-compose.yml` and the 11.4 image were **not executed** where the project was finalized (no Docker): the compose file was only checked syntactically.
* Duration is wall-clock, including time spent waiting for a metadata lock.
* `sweep.sh` needs Bash; there is no native PowerShell version (use Git Bash or WSL).

## 17. Reproducibility

* Pinned image `mariadb:11.4`; all settings in `docker-compose.yml` and `.env`; dataset deterministic (`--seed`, default 42).
* `sweep_config.txt` in every sweep folder records server version, buffer pool, rows, phases, threads, interval, timestamps.
* Every ALTER row stores the exact SQL, session configuration, server version and dataset size.
* To redo everything: `docker compose down -v && docker compose up -d`, then `./sweep.sh --rows 1000000 --repeats 3`.
* Reported runs should state the machine, Docker resources and buffer pool size.

## 18. Team

| Area | Owner | Main files | Original research items |
|---|---|---|---|
| Infrastructure, progress polling, widen-column | Bashah | `docker-compose.yml`, `schema.sql`, `generate_data.py`, processlist polling in `run_alter.py`, `widen-column-*` | Does INSTANT/NOCOPY work for widening a VARCHAR? |
| `workload.py`, add-index | Leyla | `workload.py`, `add-index` | Does adding an index support NOCOPY; how does it differ from INPLACE? |
| `run_alter.py` skeleton, change-type | Mirqe | `run_alter.py`, `experiments.py`, `change-type` | Widening/changing types (DATE → DATETIME tested) |
| README, sweep script, add-fk | Yasmine | `README.md`, `sweep.sh`, `tests/add-fk/`, `add-fk*` | Does MariaDB support INPLACE/NOCOPY for a foreign key, or force COPY? |

The research items are answered *indicatively* in [15. Findings](#15-findings) and definitively only once the 11.4 benchmark has run.

## 19. Project Structure

```text
MyLYMB_database_project/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml          MariaDB 11.4, localhost-only, healthcheck
├── requirements.txt
├── schema.sql                  user_table + orders (re-runnable)
├── common.py                   config (.env / environment), connection, UTC timestamps
├── experiments.py              CHANGES and ALGORITHMS registry
├── generate_data.py            deterministic streaming data generator
├── reset_db.py                 schema + data = identical baseline
├── workload.py                 concurrent INSERT/UPDATE/DELETE with latency CSV
├── run_alter.py                one timed ALTER + processlist polling
├── analyze_results.py          statistics by phase + figures
├── sweep.sh                    full matrix automation
├── docs/
│   ├── methodology.md
│   └── experiments.md
├── tests/add-fk/               manual SQL scenarios
├── results/
│   ├── historical/             original preliminary CSVs (unchanged)
│   └── validation_sandbox_mariadb10.11/   pipeline validation run (NOT the 11.4 benchmark)
└── reports/
    ├── PROJECT_CHANGELOG_AND_ANALYSIS.pdf
    └── make_report.py
```

## 20. Lessons Learned

* Reset between runs is not optional: a successful change-type makes the next identical change-type a no-op.
* A refused ALTER is data. Recording errno and message turned "bugs" into the most informative part of the matrix.
* `foreign_key_checks` is a session setting, so it belongs in the experiment definition, not in the algorithm list.
* Sub-second ALTERs on small tables overlap only a handful of workload statements; p95 needs big tables and repetitions.
* Sharing one runner, one timestamp format (UTC) and one CSV schema is what makes the results comparable.
* Primary-key access in the workload keeps the measurement about DDL interference, not table scans.

## 21. Conclusion

The project now provides a reproducible method to answer its research question: a deterministic dataset, a
reset before every run, a concurrent write workload, a single runner for all schema changes and algorithms,
and an analysis that separates baseline, ALTER window and recovery. The validation run shows that the method
distinguishes refused, blocking and non-blocking outcomes, and already points to a clear contrast between
table-copy ALTERs, which held writes for their whole duration, and in-place/no-copy/instant ALTERs, which did not.
Those observations come from MariaDB 10.11 with small samples; the academic conclusion on MariaDB 11.4
still requires running `./sweep.sh --rows 1000000 --repeats 3` on the pinned Docker image.
