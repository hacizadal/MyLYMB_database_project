# Analysis of sweep_20261116_160234

- Server: `11.4.13-MariaDB-ubu2404`
- Dataset rows (target table): 100000
- ALTER runs: 8  (success: 7, failure: 1)

## ALTER duration and outcome

`expected_rejection` means error 1846 for a deliberately incompatible request; it is not a successful ALTER. Other errors are `unexpected_failure`.

Single-run standard deviation is undefined; do not infer performance rankings from 1,000-row smoke tests.

| change | algorithm | runs | successes | failures | expected_rejections | unexpected_failures | stddev_s | p25_s | p75_s | mean_s | median_s | min_s | max_s | first_error |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add-index | copy | 1 | 1 | 0 | 0 | 0 |  | 0.518 | 0.518 | 0.518 | 0.518 | 0.518 | 0.518 |  |
| add-index | inplace | 1 | 1 | 0 | 0 | 0 |  | 0.137 | 0.137 | 0.137 | 0.137 | 0.137 | 0.137 |  |
| add-index | nocopy | 1 | 1 | 0 | 0 | 0 |  | 0.097 | 0.097 | 0.097 | 0.097 | 0.097 | 0.097 |  |
| add-index | instant | 1 | 0 | 1 | 1 | 0 |  |  |  |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: ADD INDEX. Try ALGORITHM=NOCOPY') |
| widen-column-60 | copy | 1 | 1 | 0 | 0 | 0 |  | 0.641 | 0.641 | 0.641 | 0.641 | 0.641 | 0.641 |  |
| widen-column-60 | inplace | 1 | 1 | 0 | 0 | 0 |  | 0.043 | 0.043 | 0.043 | 0.043 | 0.043 | 0.043 |  |
| widen-column-60 | nocopy | 1 | 1 | 0 | 0 | 0 |  | 0.029 | 0.029 | 0.029 | 0.029 | 0.029 | 0.029 |  |
| widen-column-60 | instant | 1 | 1 | 0 | 0 | 0 |  | 0.044 | 0.044 | 0.044 | 0.044 | 0.044 | 0.044 |  |


## Workload latency per phase (ms)

`low_sample=True` means fewer than 30 statements in that phase: percentiles are not meaningful (typically the ALTER was too short to overlap many workload statements; use a larger dataset).

| change | algorithm | alter_status | operation | phase | count | low_sample | success | errors | avg_ms | p50_ms | p95_ms | p99_ms | max_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| add-index | copy | success | DELETE | after | 52 | False | 52 | 0 | 4.51 | 3.71 | 6.67 | 21.22 | 28.76 |
| add-index | copy | success | DELETE | baseline | 89 | False | 89 | 0 | 3.62 | 3.45 | 4.58 | 9.44 | 10.08 |
| add-index | copy | success | DELETE | during | 7 | True | 7 | 0 | 3.21 | 3.32 | 3.81 | 3.85 | 3.85 |
| add-index | copy | success | INSERT | after | 51 | False | 51 | 0 | 14.03 | 9.64 | 54.65 | 63.74 | 63.77 |
| add-index | copy | success | INSERT | baseline | 139 | False | 139 | 0 | 9.67 | 8.53 | 11.82 | 59.55 | 88.38 |
| add-index | copy | success | INSERT | during | 8 | True | 8 | 0 | 5.43 | 4.15 | 9.79 | 11.09 | 11.41 |
| add-index | copy | success | UPDATE | after | 52 | False | 52 | 0 | 4.98 | 3.77 | 9.84 | 39.42 | 64.65 |
| add-index | copy | success | UPDATE | baseline | 139 | False | 139 | 0 | 3.03 | 3.14 | 5.62 | 8.64 | 19.23 |
| add-index | copy | success | UPDATE | during | 7 | True | 7 | 0 | 2.76 | 2.88 | 3.45 | 3.46 | 3.47 |
| add-index | inplace | success | DELETE | after | 60 | False | 60 | 0 | 5.27 | 5.23 | 6.56 | 7.04 | 7.22 |
| add-index | inplace | success | DELETE | baseline | 86 | False | 86 | 0 | 5.07 | 4.26 | 8.20 | 18.66 | 45.63 |
| add-index | inplace | success | DELETE | during | 2 | True | 2 | 0 | 4.07 | 4.07 | 4.56 | 4.61 | 4.62 |
| add-index | inplace | success | INSERT | after | 60 | False | 60 | 0 | 10.65 | 10.45 | 12.39 | 28.10 | 44.98 |
| add-index | inplace | success | INSERT | baseline | 136 | False | 136 | 0 | 10.97 | 9.51 | 20.74 | 53.07 | 67.82 |
| add-index | inplace | success | INSERT | during | 2 | True | 2 | 0 | 5.04 | 5.04 | 5.98 | 6.06 | 6.08 |
| add-index | inplace | success | UPDATE | after | 60 | False | 60 | 0 | 4.75 | 5.21 | 7.89 | 8.07 | 8.15 |
| add-index | inplace | success | UPDATE | baseline | 136 | False | 136 | 0 | 4.09 | 3.27 | 9.08 | 25.86 | 45.22 |
| add-index | inplace | success | UPDATE | during | 2 | True | 2 | 0 | 1.88 | 1.88 | 2.24 | 2.27 | 2.28 |
| add-index | nocopy | success | DELETE | after | 62 | False | 62 | 0 | 4.60 | 3.62 | 5.46 | 27.42 | 43.91 |
| add-index | nocopy | success | DELETE | baseline | 84 | False | 84 | 0 | 5.20 | 4.78 | 8.71 | 15.87 | 16.30 |
| add-index | nocopy | success | DELETE | during | 2 | True | 2 | 0 | 3.11 | 3.11 | 3.13 | 3.14 | 3.14 |
| add-index | nocopy | success | INSERT | after | 62 | False | 62 | 0 | 10.85 | 8.96 | 14.31 | 60.25 | 86.83 |
| add-index | nocopy | success | INSERT | baseline | 134 | False | 134 | 0 | 11.95 | 10.21 | 19.60 | 57.93 | 107.88 |
| add-index | nocopy | success | INSERT | during | 2 | True | 2 | 0 | 4.33 | 4.33 | 4.66 | 4.68 | 4.69 |
| add-index | nocopy | success | UPDATE | after | 62 | False | 62 | 0 | 5.19 | 3.71 | 6.40 | 53.15 | 67.06 |
| add-index | nocopy | success | UPDATE | baseline | 134 | False | 134 | 0 | 4.56 | 3.91 | 8.86 | 16.82 | 37.64 |
| add-index | nocopy | success | UPDATE | during | 2 | True | 2 | 0 | 2.00 | 2.00 | 2.78 | 2.85 | 2.87 |
| add-index | instant | failure | DELETE | after | 60 | False | 60 | 0 | 5.40 | 5.32 | 7.58 | 10.39 | 13.35 |
| add-index | instant | failure | DELETE | baseline | 87 | False | 87 | 0 | 4.93 | 4.48 | 7.67 | 13.14 | 14.30 |
| add-index | instant | failure | DELETE | during | 1 | True | 1 | 0 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 |
| add-index | instant | failure | INSERT | after | 60 | False | 60 | 0 | 10.71 | 10.27 | 15.18 | 25.45 | 36.23 |
| add-index | instant | failure | INSERT | baseline | 137 | False | 137 | 0 | 10.56 | 9.10 | 15.50 | 45.26 | 87.14 |
| add-index | instant | failure | INSERT | during | 1 | True | 1 | 0 | 5.08 | 5.08 | 5.08 | 5.08 | 5.08 |
| add-index | instant | failure | UPDATE | after | 60 | False | 60 | 0 | 4.73 | 4.28 | 7.42 | 10.20 | 13.78 |
| add-index | instant | failure | UPDATE | baseline | 137 | False | 137 | 0 | 3.94 | 3.72 | 7.69 | 12.73 | 30.70 |
| add-index | instant | failure | UPDATE | during | 1 | True | 1 | 0 | 1.59 | 1.59 | 1.59 | 1.59 | 1.59 |
| widen-column-60 | copy | success | DELETE | after | 53 | False | 53 | 0 | 5.60 | 5.20 | 8.51 | 12.21 | 12.97 |
| widen-column-60 | copy | success | DELETE | baseline | 87 | False | 87 | 0 | 5.39 | 5.02 | 8.32 | 13.28 | 30.63 |
| widen-column-60 | copy | success | DELETE | during | 8 | True | 8 | 0 | 4.89 | 4.81 | 6.57 | 7.08 | 7.21 |
| widen-column-60 | copy | success | INSERT | after | 52 | False | 52 | 0 | 11.62 | 10.42 | 19.91 | 24.50 | 25.72 |
| widen-column-60 | copy | success | INSERT | baseline | 137 | False | 137 | 0 | 10.81 | 9.94 | 16.32 | 25.21 | 62.04 |
| widen-column-60 | copy | success | INSERT | during | 9 | True | 9 | 0 | 6.21 | 6.54 | 7.62 | 7.84 | 7.89 |
| widen-column-60 | copy | success | UPDATE | after | 53 | False | 53 | 0 | 7.61 | 5.32 | 12.17 | 71.85 | 78.92 |
| widen-column-60 | copy | success | UPDATE | baseline | 137 | False | 137 | 0 | 4.41 | 4.15 | 8.09 | 12.66 | 26.63 |
| widen-column-60 | copy | success | UPDATE | during | 8 | True | 8 | 0 | 3.27 | 3.60 | 4.70 | 4.91 | 4.96 |
| widen-column-60 | inplace | success | DELETE | after | 61 | False | 61 | 0 | 6.34 | 5.53 | 12.57 | 14.90 | 17.05 |
| widen-column-60 | inplace | success | DELETE | baseline | 87 | False | 87 | 0 | 5.60 | 5.09 | 8.15 | 11.56 | 14.10 |
| widen-column-60 | inplace | success | INSERT | after | 61 | False | 61 | 0 | 11.94 | 10.54 | 17.02 | 43.89 | 63.44 |
| widen-column-60 | inplace | success | INSERT | baseline | 137 | False | 137 | 0 | 11.85 | 10.58 | 18.17 | 39.49 | 49.56 |
| widen-column-60 | inplace | success | UPDATE | after | 61 | False | 61 | 0 | 7.39 | 4.85 | 13.36 | 63.49 | 106.30 |
| widen-column-60 | inplace | success | UPDATE | baseline | 137 | False | 137 | 0 | 4.44 | 4.54 | 8.01 | 10.63 | 23.61 |
| widen-column-60 | nocopy | success | DELETE | after | 64 | False | 64 | 0 | 5.36 | 5.09 | 8.61 | 11.98 | 12.80 |
| widen-column-60 | nocopy | success | DELETE | baseline | 84 | False | 84 | 0 | 5.83 | 5.23 | 9.05 | 22.58 | 32.81 |
| widen-column-60 | nocopy | success | INSERT | after | 64 | False | 64 | 0 | 11.65 | 9.85 | 22.28 | 44.50 | 50.02 |
| widen-column-60 | nocopy | success | INSERT | baseline | 134 | False | 134 | 0 | 11.79 | 10.26 | 19.27 | 39.72 | 97.59 |
| widen-column-60 | nocopy | success | UPDATE | after | 64 | False | 64 | 0 | 5.21 | 5.21 | 9.24 | 16.92 | 23.25 |
| widen-column-60 | nocopy | success | UPDATE | baseline | 134 | False | 134 | 0 | 4.88 | 4.48 | 9.03 | 19.69 | 35.42 |
| widen-column-60 | instant | success | DELETE | after | 64 | False | 64 | 0 | 6.25 | 5.37 | 10.05 | 25.96 | 49.98 |
| widen-column-60 | instant | success | DELETE | baseline | 83 | False | 83 | 0 | 6.18 | 5.23 | 7.18 | 22.10 | 62.94 |
| widen-column-60 | instant | success | DELETE | during | 1 | True | 1 | 0 | 3.93 | 3.93 | 3.93 | 3.93 | 3.93 |
| widen-column-60 | instant | success | INSERT | after | 64 | False | 64 | 0 | 10.99 | 10.18 | 19.06 | 29.49 | 36.36 |
| widen-column-60 | instant | success | INSERT | baseline | 133 | False | 133 | 0 | 10.87 | 10.30 | 14.04 | 22.51 | 68.95 |
| widen-column-60 | instant | success | INSERT | during | 1 | True | 1 | 0 | 9.84 | 9.84 | 9.84 | 9.84 | 9.84 |
| widen-column-60 | instant | success | UPDATE | after | 64 | False | 64 | 0 | 5.12 | 4.89 | 7.75 | 19.38 | 36.91 |
| widen-column-60 | instant | success | UPDATE | baseline | 133 | False | 133 | 0 | 6.00 | 4.84 | 7.48 | 61.40 | 67.37 |
| widen-column-60 | instant | success | UPDATE | during | 1 | True | 1 | 0 | 4.30 | 4.30 | 4.30 | 4.30 | 4.30 |


## Figures

- fig_alter_duration.png
- fig_workload_p95.png
- fig_latency_distribution.png
- fig_workload_errors.png: not generated (no applicable data)
