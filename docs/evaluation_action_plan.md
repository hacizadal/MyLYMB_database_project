# Evaluator feedback: action plan and verification status

## Research question

How do MariaDB 11.4 native DDL algorithms (`INSTANT`, `NOCOPY`, `INPLACE`, and `COPY, LOCK=NONE`) compare in migration time, write latency and concurrent-write availability under an identical reproducible workload?

## What is implemented

- The existing deterministic reset, concurrent DML workload, processlist sampling, and CSV reporting are preserved.
- `COPY, LOCK=NONE` is now described as a MariaDB 11.2+ feature rather than as a universally unsupported operation.
- The experiment matrix already includes `INSTANT`, `NOCOPY`, `INPLACE`, `COPY`, default, and explicit blocking baselines.
- `add-index` with `INSTANT` is a negative test candidate for error 1846. **Capture and report the actual server code/message; do not assume the result.**
- Unit tests cover the SQL matrix and the negative-test candidate.

## Primary experiment (not yet executed in this environment)

1. `docker compose up -d --wait` and verify `SELECT VERSION()` reports 11.4.x.
2. `python -m pytest -q`.
3. `./sweep.sh --rows 1000 --repeats 1` for a smoke test.
4. `./sweep.sh --rows 1000000 --repeats 3 --sweep-id primary_11_4` for the primary comparison; budget sufficient time and disk space.
5. Run `python analyze_results.py --help` and follow the supported arguments to produce analysis.
6. Record CPU, RAM, disk, Docker version, MariaDB patch version, and workload settings.
7. Verify each result against raw CSV files and retain failed operations with their exact error codes.

## Interpretation and limitations

- A requested algorithm is not necessarily an algorithm the server can execute. Refusal is a valid finding.
- Online DDL can still wait for metadata locks; `LOCK=NONE` is not a guarantee of zero waiting.
- The older MariaDB 10.11.14 sandbox measurements are **historical validation only**, not 11.4 results.
- Results on a single host and synthetic workload cannot be generalized to every production system.
- Replication lag is not measured by the current single-server Docker Compose configuration. Do not claim replication results.

## Remaining work

Run and validate the actual MariaDB 11.4 benchmarks; include charts and statistical summaries from the resulting CSVs; add a replication environment if replication is required for the final submission.
