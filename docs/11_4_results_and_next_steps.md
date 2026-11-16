# MariaDB 11.4.13: observed smoke-test results and remaining research

## Provenance and scope

The team ran `PYTHON=python bash sweep.sh --rows 1000 --repeats 1` on Windows Git Bash with Docker `mariadb:11.4`; `SELECT VERSION()` returned `11.4.13-MariaDB-ubu2404`. The console output was shared on 2026-11-16. **The underlying CSVs were not included in this distribution.** These figures are transcribed from the terminal output and must not be described as independently re-run or statistically significant. The full results directory should be committed separately after review.

## Compatibility observations (42 requests)

* 32 ALTERs succeeded; 10 returned error 1846 (unsupported algorithm).
* `change-type`: COPY/default succeeded; INPLACE, NOCOPY and INSTANT returned 1846.
* `add-index`: COPY, INPLACE and NOCOPY succeeded; INSTANT returned 1846 (`ADD INDEX`, suggests NOCOPY).
* Both VARCHAR-widening cases succeeded with all seven requested algorithm configurations on this schema.
* `add-fk` with checks ON: INPLACE, NOCOPY and INSTANT returned 1846. With `foreign_key_checks=OFF`, INPLACE and NOCOPY succeeded but INSTANT returned 1846.
* `widen-column-60`: INSTANT 0.024 s versus COPY 0.100 s **in one run**. This is not evidence of a general 4x speedup.

An error 1846 is a useful negative test, not proof of a broken benchmark. `foreign_key_checks=OFF` removes validation of existing rows; it is **not** a safe general-purpose performance shortcut.

## Missing evidence before a final claim

1. Run `PYTHON=python bash sweep.sh --rows 100000 --repeats 3` on the target machine, then 1,000,000 rows if feasible.
2. Preserve the entire output directory including `sweep_config.txt`, `alter_results.csv`, `workload_*.csv`, and `analysis/`.
3. Record CPU, RAM, storage type, Docker limits, exact MariaDB version and host OS. Repetitions should be compared at equal workload settings.
4. Examine baseline/during/after write p95 and error counts. Very short ALTER windows may contain too few samples to support p95 claims; the analysis marks these `low_sample`.
5. Add a separate, carefully controlled metadata-lock waiting experiment and, if feasible, a replication experiment. Neither is claimed as completed here.

## Limitations

The 1,000-row dataset is a **compatibility smoke test**, not a performance benchmark. Wall-clock timings include client and scheduling overhead. `ALGORITHM=DEFAULT` is server-selected, not guaranteed to be COPY; `COPY, LOCK=NONE` is explicitly requested. The harness observes lock waits via periodic processlist polling, which can miss short waits. Disabling foreign-key checks can allow invalid historical references. No replica was measured in this run.
