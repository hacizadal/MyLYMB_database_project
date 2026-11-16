# MariaDB 11.4.13 — repeated 100,000-row benchmark (terminal evidence)

**Source:** Team-provided Git Bash terminal transcript, 2026-11-16; run identifier `sweep_20261116_145509`. Command: `PYTHON=python bash sweep.sh --rows 100000 --repeats 3`. The previously observed container version was `11.4.13-MariaDB-ubu2404`; the pasted transcript itself does not independently print `SELECT VERSION()`. The full raw output is preserved in `terminal_output.txt`.

**Results:** 126 ALTER requests = 6 changes × 7 algorithm choices × 3 repetitions. **102 successes, 24 expected error-1846 rejections, 0 unexpected DDL errors** in the console transcript. The 24 rejections are valid compatibility observations, not failed execution of the experiment.

The machine specifications and original per-statement workload CSV files **were not supplied**. This distribution therefore contains a *terminal-derived transcription*, not the original `alter_results.csv`, workload traces, or original generated analysis. The CSVs here are labeled `console_*` to prevent confusion. Do not claim measured concurrent-write throughput, p95 latency, write error rates, lock-wait distributions, or replica behavior from these data.

## Representative measurements

| Change | Algorithm | Mean ALTER seconds (n=3) | Outcome |
|---|---|---:|---|
| Widen VARCHAR to 60 | INSTANT | 0.0277 | 3 successes |
| Widen VARCHAR to 60 | COPY | 0.4313 | 3 successes |
| Widen VARCHAR to 100 | INSTANT | 0.0267 | 3 successes |
| Widen VARCHAR to 100 | COPY | 0.4117 | 3 successes |
| Add secondary index | NOCOPY | 0.1280 | 3 successes |
| Add secondary index | COPY | 0.4623 | 3 successes |
| Change DATE to DATETIME | COPY | 0.5303 | 3 successes |
| Add foreign key, checks ON | COPY | 0.7550 | 3 successes |
| Add foreign key, checks OFF | NOCOPY | 0.1320 | 3 successes |

See `console_alter_summary.csv` for **all 42 combinations**, including sample standard deviations and minimum/maximum. See `console_alter_runs.csv` for the **126 individual timings** and exact rejection messages. The plot `console_duration_comparison.png` excludes unsupported algorithm/change pairs (marked N/A).

In this particular benchmark, widening to 60 was about **15.6× faster** with INSTANT than with COPY on mean DDL wall time; adding an index was about **3.6× faster** with NOCOPY than with COPY. These ratios do not establish production performance or write availability. Three repetitions on one machine give limited uncertainty estimates.

## Compatibility and interpretation

* `change-type`: INPLACE, NOCOPY, INSTANT refused with error 1846; COPY succeeds.
* `add-index`: INSTANT refused (MariaDB suggests NOCOPY).
* Both widening cases: all seven requested configurations succeeded.
* `add-fk` with foreign-key checks ON: INPLACE, NOCOPY, INSTANT refused; with checks OFF: INPLACE and NOCOPY succeeded, INSTANT still refused because index creation is needed.
* `foreign_key_checks=OFF` can skip validation of existing rows; it is not an unconditional recommendation.
* `DEFAULT` chooses an algorithm; it must not be assumed equivalent to COPY. The explicit `COPY, LOCK=NONE` result is of particular interest on 11.4.

## What is still required for a full online-write claim

Copy the actual `results/sweep_20261116_145509/` directory from the testing laptop, including `alter_results.csv`, `workload_*.csv`, `sweep_config.txt`, and `analysis/`. Then run `python analyze_results.py results/sweep_20261116_145509` and inspect per-phase sample counts, errors, throughput and latency. Document hardware and Docker resource limits. Metadata-lock contention and replication experiments have **not** been performed or claimed in this distribution.
