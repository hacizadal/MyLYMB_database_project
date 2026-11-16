# Analysis of sandbox_mariadb11.4_1M

- Server: `11.4.9-MariaDB`
- Dataset rows (target table): 1000000
- ALTER runs: 49  (success: 38, failure: 11)

## ALTER duration and outcome

| change | algorithm | runs | successes | failures | mean_s | median_s | min_s | max_s | first_error |
|---|---|---|---|---|---|---|---|---|---|
| change-type | default | 1 | 1 | 0 | 2.685 | 2.685 | 2.685 | 2.685 |  |
| change-type | blocking | 1 | 1 | 0 | 2.658 | 2.658 | 2.658 | 2.658 |  |
| change-type | copy | 1 | 1 | 0 | 3.304 | 3.304 | 3.304 | 3.304 |  |
| change-type | copy-shared | 1 | 1 | 0 | 2.748 | 2.748 | 2.748 | 2.748 |  |
| change-type | inplace | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INPLACE is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| change-type | nocopy | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=NOCOPY is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| change-type | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| add-index | default | 1 | 1 | 0 | 1.099 | 1.099 | 1.099 | 1.099 |  |
| add-index | blocking | 1 | 1 | 0 | 3.329 | 3.329 | 3.329 | 3.329 |  |
| add-index | copy | 1 | 1 | 0 | 3.162 | 3.162 | 3.162 | 3.162 |  |
| add-index | copy-shared | 1 | 1 | 0 | 2.956 | 2.956 | 2.956 | 2.956 |  |
| add-index | inplace | 1 | 1 | 0 | 0.912 | 0.912 | 0.912 | 0.912 |  |
| add-index | nocopy | 1 | 1 | 0 | 0.677 | 0.677 | 0.677 | 0.677 |  |
| add-index | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: ADD INDEX. Try ALGORITHM=NOCOPY') |
| widen-column-60 | default | 1 | 1 | 0 | 0.004 | 0.004 | 0.004 | 0.004 |  |
| widen-column-60 | blocking | 1 | 1 | 0 | 2.513 | 2.513 | 2.513 | 2.513 |  |
| widen-column-60 | copy | 1 | 1 | 0 | 2.377 | 2.377 | 2.377 | 2.377 |  |
| widen-column-60 | copy-shared | 1 | 1 | 0 | 2.498 | 2.498 | 2.498 | 2.498 |  |
| widen-column-60 | inplace | 1 | 1 | 0 | 0.012 | 0.012 | 0.012 | 0.012 |  |
| widen-column-60 | nocopy | 1 | 1 | 0 | 0.010 | 0.010 | 0.010 | 0.010 |  |
| widen-column-60 | instant | 1 | 1 | 0 | 0.004 | 0.004 | 0.004 | 0.004 |  |
| widen-column-100 | default | 1 | 1 | 0 | 0.012 | 0.012 | 0.012 | 0.012 |  |
| widen-column-100 | blocking | 1 | 1 | 0 | 2.731 | 2.731 | 2.731 | 2.731 |  |
| widen-column-100 | copy | 1 | 1 | 0 | 2.333 | 2.333 | 2.333 | 2.333 |  |
| widen-column-100 | copy-shared | 1 | 1 | 0 | 2.514 | 2.514 | 2.514 | 2.514 |  |
| widen-column-100 | inplace | 1 | 1 | 0 | 0.004 | 0.004 | 0.004 | 0.004 |  |
| widen-column-100 | nocopy | 1 | 1 | 0 | 0.010 | 0.010 | 0.010 | 0.010 |  |
| widen-column-100 | instant | 1 | 1 | 0 | 0.005 | 0.005 | 0.005 | 0.005 |  |
| widen-column-rebuild | default | 1 | 1 | 0 | 2.471 | 2.471 | 2.471 | 2.471 |  |
| widen-column-rebuild | blocking | 1 | 1 | 0 | 2.524 | 2.524 | 2.524 | 2.524 |  |
| widen-column-rebuild | copy | 1 | 1 | 0 | 2.246 | 2.246 | 2.246 | 2.246 |  |
| widen-column-rebuild | copy-shared | 1 | 1 | 0 | 2.606 | 2.606 | 2.606 | 2.606 |  |
| widen-column-rebuild | inplace | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INPLACE is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| widen-column-rebuild | nocopy | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=NOCOPY is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| widen-column-rebuild | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| add-fk | default | 1 | 1 | 0 | 6.426 | 6.426 | 6.426 | 6.426 |  |
| add-fk | blocking | 1 | 1 | 0 | 6.573 | 6.573 | 6.573 | 6.573 |  |
| add-fk | copy | 1 | 1 | 0 | 7.217 | 7.217 | 7.217 | 7.217 |  |
| add-fk | copy-shared | 1 | 1 | 0 | 7.195 | 7.195 | 7.195 | 7.195 |  |
| add-fk | inplace | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INPLACE is not supported. Reason: Adding foreign keys needs foreign_key_checks=OFF. Try ALGORITHM=COPY') |
| add-fk | nocopy | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=NOCOPY is not supported. Reason: Adding foreign keys needs foreign_key_checks=OFF. Try ALGORITHM=COPY') |
| add-fk | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: Adding foreign keys needs foreign_key_checks=OFF. Try ALGORITHM=COPY') |
| add-fk-fkchecks-off | default | 1 | 1 | 0 | 0.868 | 0.868 | 0.868 | 0.868 |  |
| add-fk-fkchecks-off | blocking | 1 | 1 | 0 | 2.356 | 2.356 | 2.356 | 2.356 |  |
| add-fk-fkchecks-off | copy | 1 | 1 | 0 | 2.080 | 2.080 | 2.080 | 2.080 |  |
| add-fk-fkchecks-off | copy-shared | 1 | 1 | 0 | 2.649 | 2.649 | 2.649 | 2.649 |  |
| add-fk-fkchecks-off | inplace | 1 | 1 | 0 | 0.815 | 0.815 | 0.815 | 0.815 |  |
| add-fk-fkchecks-off | nocopy | 1 | 1 | 0 | 0.933 | 0.933 | 0.933 | 0.933 |  |
| add-fk-fkchecks-off | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: ADD INDEX. Try ALGORITHM=NOCOPY') |


## Workload latency per phase (ms)

`low_sample=True` means fewer than 30 statements in that phase: percentiles are not meaningful (typically the ALTER was too short to overlap many workload statements; use a larger dataset).

| change | algorithm | alter_status | operation | phase | count | low_sample | success | errors | avg_ms | p50_ms | p95_ms | p99_ms | max_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| change-type | default | success | DELETE | after | 114 | False | 114 | 0 | 0.73 | 0.63 | 1.09 | 1.88 | 6.77 |
| change-type | default | success | DELETE | baseline | 96 | False | 96 | 0 | 0.81 | 0.64 | 1.24 | 4.42 | 5.21 |
| change-type | default | success | DELETE | during | 72 | False | 72 | 0 | 5.37 | 1.39 | 21.29 | 59.80 | 64.92 |
| change-type | default | success | INSERT | after | 114 | False | 114 | 0 | 1.73 | 1.48 | 2.73 | 5.85 | 13.07 |
| change-type | default | success | INSERT | baseline | 196 | False | 196 | 0 | 1.69 | 1.52 | 2.51 | 6.80 | 9.22 |
| change-type | default | success | INSERT | during | 72 | False | 72 | 0 | 16.57 | 6.73 | 49.62 | 64.04 | 69.93 |
| change-type | default | success | UPDATE | after | 114 | False | 114 | 0 | 0.70 | 0.72 | 1.20 | 1.28 | 1.41 |
| change-type | default | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.65 | 0.62 | 1.13 | 1.97 | 2.63 |
| change-type | default | success | UPDATE | during | 72 | False | 72 | 0 | 2.78 | 1.50 | 12.56 | 26.33 | 27.13 |
| change-type | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.71 | 0.63 | 1.03 | 2.09 | 4.56 |
| change-type | blocking | success | DELETE | baseline | 98 | False | 98 | 0 | 0.66 | 0.59 | 0.98 | 2.70 | 3.08 |
| change-type | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.62 | 1.49 | 2.22 | 4.17 | 7.04 |
| change-type | blocking | success | INSERT | baseline | 198 | False | 198 | 0 | 1.48 | 1.46 | 2.06 | 3.30 | 4.15 |
| change-type | blocking | success | INSERT | during | 2 | True | 2 | 0 | 2608.73 | 2608.73 | 2608.92 | 2608.94 | 2608.94 |
| change-type | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.80 | 0.68 | 1.80 | 4.61 | 5.71 |
| change-type | blocking | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.60 | 0.54 | 1.09 | 1.29 | 5.10 |
| change-type | copy | success | DELETE | after | 114 | False | 114 | 0 | 0.69 | 0.59 | 1.21 | 2.07 | 4.84 |
| change-type | copy | success | DELETE | baseline | 100 | False | 100 | 0 | 0.85 | 0.67 | 1.97 | 3.50 | 4.86 |
| change-type | copy | success | DELETE | during | 91 | False | 91 | 0 | 3.94 | 1.15 | 22.94 | 44.58 | 54.84 |
| change-type | copy | success | INSERT | after | 114 | False | 114 | 0 | 1.72 | 1.43 | 2.88 | 11.24 | 13.28 |
| change-type | copy | success | INSERT | baseline | 200 | False | 200 | 0 | 1.53 | 1.45 | 2.11 | 2.65 | 4.72 |
| change-type | copy | success | INSERT | during | 91 | False | 91 | 0 | 13.61 | 4.68 | 47.44 | 111.70 | 116.81 |
| change-type | copy | success | UPDATE | after | 114 | False | 114 | 0 | 0.73 | 0.66 | 1.38 | 2.26 | 3.86 |
| change-type | copy | success | UPDATE | baseline | 200 | False | 200 | 0 | 0.65 | 0.60 | 1.20 | 2.40 | 4.78 |
| change-type | copy | success | UPDATE | during | 91 | False | 91 | 0 | 4.00 | 1.04 | 24.20 | 49.46 | 59.53 |
| change-type | copy-shared | success | DELETE | after | 114 | False | 114 | 0 | 0.85 | 0.73 | 1.42 | 3.45 | 3.92 |
| change-type | copy-shared | success | DELETE | baseline | 96 | False | 96 | 0 | 0.71 | 0.65 | 1.13 | 1.54 | 2.72 |
| change-type | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.77 | 1.55 | 2.70 | 9.20 | 9.83 |
| change-type | copy-shared | success | INSERT | baseline | 196 | False | 196 | 0 | 1.52 | 1.49 | 2.13 | 2.68 | 3.28 |
| change-type | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 2746.11 | 2746.11 | 2751.51 | 2751.99 | 2752.11 |
| change-type | copy-shared | success | UPDATE | after | 114 | False | 114 | 0 | 0.76 | 0.73 | 1.37 | 1.77 | 2.45 |
| change-type | copy-shared | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.60 | 0.58 | 1.00 | 1.34 | 1.44 |
| change-type | inplace | failure | DELETE | after | 114 | False | 114 | 0 | 0.64 | 0.59 | 0.96 | 1.26 | 1.45 |
| change-type | inplace | failure | DELETE | baseline | 98 | False | 98 | 0 | 0.77 | 0.62 | 1.32 | 4.05 | 4.34 |
| change-type | inplace | failure | INSERT | after | 114 | False | 114 | 0 | 1.58 | 1.55 | 1.98 | 3.27 | 3.53 |
| change-type | inplace | failure | INSERT | baseline | 198 | False | 198 | 0 | 1.54 | 1.48 | 2.14 | 3.47 | 4.69 |
| change-type | inplace | failure | UPDATE | after | 114 | False | 114 | 0 | 0.63 | 0.64 | 1.04 | 1.23 | 1.34 |
| change-type | inplace | failure | UPDATE | baseline | 198 | False | 198 | 0 | 0.66 | 0.59 | 1.21 | 2.31 | 3.73 |
| change-type | nocopy | failure | DELETE | after | 114 | False | 114 | 0 | 0.64 | 0.54 | 1.31 | 2.52 | 2.90 |
| change-type | nocopy | failure | DELETE | baseline | 98 | False | 98 | 0 | 0.72 | 0.59 | 1.49 | 3.27 | 3.79 |
| change-type | nocopy | failure | INSERT | after | 114 | False | 114 | 0 | 1.56 | 1.46 | 2.18 | 3.64 | 4.48 |
| change-type | nocopy | failure | INSERT | baseline | 198 | False | 198 | 0 | 1.56 | 1.47 | 2.32 | 3.94 | 5.99 |
| change-type | nocopy | failure | UPDATE | after | 114 | False | 114 | 0 | 0.62 | 0.62 | 1.06 | 1.42 | 1.72 |
| change-type | nocopy | failure | UPDATE | baseline | 198 | False | 198 | 0 | 0.65 | 0.59 | 1.13 | 2.61 | 3.46 |
| change-type | instant | failure | DELETE | after | 114 | False | 114 | 0 | 0.76 | 0.68 | 1.48 | 1.99 | 2.17 |
| change-type | instant | failure | DELETE | baseline | 98 | False | 98 | 0 | 0.89 | 0.63 | 3.07 | 5.19 | 5.70 |
| change-type | instant | failure | INSERT | after | 114 | False | 114 | 0 | 1.63 | 1.59 | 2.22 | 3.41 | 3.59 |
| change-type | instant | failure | INSERT | baseline | 198 | False | 198 | 0 | 1.56 | 1.48 | 2.32 | 4.15 | 4.95 |
| change-type | instant | failure | UPDATE | after | 114 | False | 114 | 0 | 0.75 | 0.73 | 1.25 | 2.01 | 3.47 |
| change-type | instant | failure | UPDATE | baseline | 198 | False | 198 | 0 | 0.69 | 0.59 | 1.60 | 2.43 | 4.69 |
| add-index | default | success | DELETE | after | 114 | False | 114 | 0 | 0.76 | 0.64 | 1.60 | 3.05 | 4.54 |
| add-index | default | success | DELETE | baseline | 96 | False | 96 | 0 | 0.80 | 0.72 | 1.30 | 2.71 | 3.50 |
| add-index | default | success | DELETE | during | 36 | False | 36 | 0 | 1.40 | 1.16 | 2.28 | 5.44 | 6.83 |
| add-index | default | success | INSERT | after | 112 | False | 112 | 0 | 1.82 | 1.44 | 2.90 | 16.34 | 18.42 |
| add-index | default | success | INSERT | baseline | 196 | False | 196 | 0 | 1.67 | 1.56 | 2.42 | 4.26 | 5.55 |
| add-index | default | success | INSERT | during | 38 | False | 38 | 0 | 6.33 | 3.60 | 15.13 | 17.90 | 18.47 |
| add-index | default | success | UPDATE | after | 112 | False | 112 | 0 | 0.74 | 0.66 | 1.52 | 2.86 | 3.19 |
| add-index | default | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.67 | 0.63 | 1.21 | 2.76 | 3.46 |
| add-index | default | success | UPDATE | during | 38 | False | 38 | 0 | 2.06 | 1.32 | 6.45 | 8.52 | 8.80 |
| add-index | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.76 | 0.65 | 1.14 | 1.81 | 3.91 |
| add-index | blocking | success | DELETE | baseline | 98 | False | 98 | 0 | 0.77 | 0.65 | 1.22 | 1.58 | 7.15 |
| add-index | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.92 | 1.59 | 2.39 | 15.51 | 18.75 |
| add-index | blocking | success | INSERT | baseline | 198 | False | 198 | 0 | 1.62 | 1.52 | 2.10 | 3.80 | 6.97 |
| add-index | blocking | success | INSERT | during | 2 | True | 2 | 0 | 3294.28 | 3294.28 | 3298.29 | 3298.65 | 3298.74 |
| add-index | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.74 | 0.77 | 1.30 | 1.97 | 2.48 |
| add-index | blocking | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.66 | 0.64 | 1.16 | 1.79 | 4.50 |
| add-index | copy | success | DELETE | after | 114 | False | 114 | 0 | 0.83 | 0.76 | 1.24 | 2.40 | 2.64 |
| add-index | copy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.67 | 0.61 | 1.01 | 1.45 | 2.13 |
| add-index | copy | success | DELETE | during | 84 | False | 84 | 0 | 4.96 | 1.25 | 28.33 | 46.66 | 56.48 |
| add-index | copy | success | INSERT | after | 114 | False | 114 | 0 | 1.72 | 1.65 | 2.32 | 2.94 | 4.34 |
| add-index | copy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.65 | 1.52 | 2.83 | 4.63 | 5.16 |
| add-index | copy | success | INSERT | during | 84 | False | 84 | 0 | 15.20 | 5.84 | 59.39 | 83.40 | 83.43 |
| add-index | copy | success | UPDATE | after | 114 | False | 114 | 0 | 0.75 | 0.74 | 1.32 | 1.83 | 3.59 |
| add-index | copy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.61 | 0.56 | 1.08 | 1.33 | 1.53 |
| add-index | copy | success | UPDATE | during | 84 | False | 84 | 0 | 4.50 | 1.23 | 8.88 | 67.51 | 78.04 |
| add-index | copy-shared | success | DELETE | after | 114 | False | 114 | 0 | 0.81 | 0.56 | 1.25 | 8.87 | 10.51 |
| add-index | copy-shared | success | DELETE | baseline | 98 | False | 98 | 0 | 0.64 | 0.57 | 1.00 | 2.52 | 2.55 |
| add-index | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.55 | 1.51 | 2.12 | 2.66 | 2.77 |
| add-index | copy-shared | success | INSERT | baseline | 198 | False | 198 | 0 | 1.49 | 1.43 | 2.17 | 3.69 | 4.09 |
| add-index | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 2909.35 | 2909.35 | 2910.10 | 2910.16 | 2910.18 |
| add-index | copy-shared | success | UPDATE | after | 114 | False | 114 | 0 | 0.66 | 0.64 | 1.13 | 1.72 | 2.05 |
| add-index | copy-shared | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.59 | 0.54 | 0.97 | 1.21 | 2.66 |
| add-index | inplace | success | DELETE | after | 114 | False | 114 | 0 | 0.64 | 0.64 | 1.00 | 1.22 | 1.26 |
| add-index | inplace | success | DELETE | baseline | 96 | False | 96 | 0 | 0.73 | 0.62 | 1.32 | 2.20 | 2.41 |
| add-index | inplace | success | DELETE | during | 30 | False | 30 | 0 | 1.27 | 1.05 | 2.32 | 3.24 | 3.60 |
| add-index | inplace | success | INSERT | after | 114 | False | 114 | 0 | 1.66 | 1.57 | 2.31 | 3.30 | 3.52 |
| add-index | inplace | success | INSERT | baseline | 196 | False | 196 | 0 | 1.71 | 1.55 | 2.25 | 5.11 | 16.64 |
| add-index | inplace | success | INSERT | during | 30 | False | 30 | 0 | 7.22 | 4.74 | 13.85 | 14.55 | 14.78 |
| add-index | inplace | success | UPDATE | after | 114 | False | 114 | 0 | 0.66 | 0.67 | 1.07 | 1.40 | 1.61 |
| add-index | inplace | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.69 | 0.64 | 1.26 | 1.66 | 2.18 |
| add-index | inplace | success | UPDATE | during | 30 | False | 30 | 0 | 1.53 | 1.29 | 4.08 | 5.83 | 6.24 |
| add-index | nocopy | success | DELETE | after | 114 | False | 114 | 0 | 0.72 | 0.68 | 1.19 | 1.80 | 2.29 |
| add-index | nocopy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.72 | 0.61 | 1.23 | 1.82 | 6.57 |
| add-index | nocopy | success | DELETE | during | 22 | True | 22 | 0 | 1.23 | 0.98 | 2.47 | 2.77 | 2.85 |
| add-index | nocopy | success | INSERT | after | 114 | False | 114 | 0 | 1.69 | 1.57 | 2.30 | 4.49 | 8.59 |
| add-index | nocopy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.60 | 1.56 | 2.17 | 4.16 | 4.71 |
| add-index | nocopy | success | INSERT | during | 22 | True | 22 | 0 | 7.98 | 3.97 | 20.81 | 25.90 | 27.25 |
| add-index | nocopy | success | UPDATE | after | 114 | False | 114 | 0 | 0.79 | 0.72 | 1.35 | 3.48 | 5.58 |
| add-index | nocopy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.62 | 0.59 | 1.14 | 1.37 | 2.08 |
| add-index | nocopy | success | UPDATE | during | 22 | True | 22 | 0 | 2.09 | 1.18 | 7.46 | 9.31 | 9.76 |
| add-index | instant | failure | DELETE | after | 114 | False | 114 | 0 | 0.65 | 0.63 | 0.95 | 1.14 | 1.21 |
| add-index | instant | failure | DELETE | baseline | 94 | False | 94 | 0 | 0.65 | 0.62 | 1.07 | 1.14 | 1.17 |
| add-index | instant | failure | INSERT | after | 114 | False | 114 | 0 | 1.69 | 1.58 | 2.54 | 3.89 | 4.35 |
| add-index | instant | failure | INSERT | baseline | 194 | False | 194 | 0 | 2.14 | 1.52 | 2.35 | 8.19 | 54.71 |
| add-index | instant | failure | UPDATE | after | 114 | False | 114 | 0 | 0.68 | 0.67 | 1.13 | 1.33 | 1.53 |
| add-index | instant | failure | UPDATE | baseline | 194 | False | 194 | 0 | 0.61 | 0.57 | 1.00 | 1.45 | 2.35 |
| widen-column-60 | default | success | DELETE | after | 114 | False | 114 | 0 | 0.71 | 0.65 | 1.22 | 1.73 | 1.84 |
| widen-column-60 | default | success | DELETE | baseline | 96 | False | 96 | 0 | 0.68 | 0.65 | 1.09 | 1.18 | 1.30 |
| widen-column-60 | default | success | INSERT | after | 114 | False | 114 | 0 | 1.65 | 1.56 | 2.26 | 4.03 | 4.54 |
| widen-column-60 | default | success | INSERT | baseline | 196 | False | 196 | 0 | 1.65 | 1.55 | 2.29 | 4.00 | 5.32 |
| widen-column-60 | default | success | UPDATE | after | 114 | False | 114 | 0 | 0.78 | 0.68 | 1.51 | 3.33 | 5.42 |
| widen-column-60 | default | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.61 | 0.57 | 1.10 | 1.67 | 1.87 |
| widen-column-60 | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.76 | 0.59 | 1.10 | 2.13 | 11.66 |
| widen-column-60 | blocking | success | DELETE | baseline | 96 | False | 96 | 0 | 0.64 | 0.59 | 1.00 | 1.46 | 1.47 |
| widen-column-60 | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.51 | 1.51 | 1.96 | 2.76 | 3.31 |
| widen-column-60 | blocking | success | INSERT | baseline | 196 | False | 196 | 0 | 1.68 | 1.60 | 2.26 | 4.34 | 4.57 |
| widen-column-60 | blocking | success | INSERT | during | 2 | True | 2 | 0 | 2515.46 | 2515.46 | 2515.70 | 2515.73 | 2515.73 |
| widen-column-60 | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.70 | 0.67 | 1.22 | 1.88 | 2.55 |
| widen-column-60 | blocking | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.63 | 0.58 | 1.17 | 1.46 | 2.18 |
| widen-column-60 | copy | success | DELETE | after | 114 | False | 114 | 0 | 0.64 | 0.53 | 0.94 | 2.56 | 5.86 |
| widen-column-60 | copy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.66 | 0.58 | 1.08 | 1.47 | 2.45 |
| widen-column-60 | copy | success | DELETE | during | 60 | False | 60 | 0 | 4.79 | 1.24 | 29.09 | 46.87 | 53.67 |
| widen-column-60 | copy | success | INSERT | after | 114 | False | 114 | 0 | 1.49 | 1.45 | 1.95 | 2.36 | 3.61 |
| widen-column-60 | copy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.59 | 1.51 | 2.12 | 3.87 | 6.41 |
| widen-column-60 | copy | success | INSERT | during | 60 | False | 60 | 0 | 19.49 | 6.66 | 72.70 | 87.70 | 91.68 |
| widen-column-60 | copy | success | UPDATE | after | 114 | False | 114 | 0 | 0.63 | 0.62 | 1.14 | 1.36 | 1.45 |
| widen-column-60 | copy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.65 | 0.59 | 1.10 | 2.78 | 3.90 |
| widen-column-60 | copy | success | UPDATE | during | 60 | False | 60 | 0 | 5.33 | 1.17 | 25.64 | 35.62 | 38.01 |
| widen-column-60 | copy-shared | success | DELETE | after | 114 | False | 114 | 0 | 0.66 | 0.65 | 0.97 | 1.15 | 1.34 |
| widen-column-60 | copy-shared | success | DELETE | baseline | 96 | False | 96 | 0 | 0.63 | 0.59 | 1.00 | 1.66 | 2.13 |
| widen-column-60 | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.72 | 1.54 | 2.23 | 9.88 | 10.79 |
| widen-column-60 | copy-shared | success | INSERT | baseline | 196 | False | 196 | 0 | 1.58 | 1.49 | 2.03 | 4.02 | 5.54 |
| widen-column-60 | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 2482.18 | 2482.18 | 2483.22 | 2483.31 | 2483.34 |
| widen-column-60 | copy-shared | success | UPDATE | after | 114 | False | 114 | 0 | 0.64 | 0.66 | 1.05 | 1.22 | 1.25 |
| widen-column-60 | copy-shared | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.63 | 0.57 | 1.12 | 1.88 | 3.68 |
| widen-column-60 | inplace | success | DELETE | after | 112 | False | 112 | 0 | 0.65 | 0.60 | 0.99 | 1.10 | 2.53 |
| widen-column-60 | inplace | success | DELETE | baseline | 94 | False | 94 | 0 | 0.74 | 0.66 | 1.31 | 1.91 | 2.31 |
| widen-column-60 | inplace | success | DELETE | during | 2 | True | 2 | 0 | 0.85 | 0.85 | 0.91 | 0.91 | 0.92 |
| widen-column-60 | inplace | success | INSERT | after | 112 | False | 112 | 0 | 1.67 | 1.57 | 2.80 | 4.35 | 4.94 |
| widen-column-60 | inplace | success | INSERT | baseline | 194 | False | 194 | 0 | 1.65 | 1.55 | 2.45 | 3.67 | 7.17 |
| widen-column-60 | inplace | success | INSERT | during | 2 | True | 2 | 0 | 1.46 | 1.46 | 1.59 | 1.60 | 1.60 |
| widen-column-60 | inplace | success | UPDATE | after | 112 | False | 112 | 0 | 0.67 | 0.69 | 1.12 | 1.52 | 1.77 |
| widen-column-60 | inplace | success | UPDATE | baseline | 194 | False | 194 | 0 | 0.67 | 0.63 | 1.17 | 2.31 | 3.66 |
| widen-column-60 | inplace | success | UPDATE | during | 2 | True | 2 | 0 | 0.92 | 0.92 | 1.46 | 1.50 | 1.52 |
| widen-column-60 | nocopy | success | DELETE | after | 114 | False | 114 | 0 | 0.75 | 0.67 | 1.21 | 2.65 | 3.79 |
| widen-column-60 | nocopy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.71 | 0.66 | 1.09 | 1.80 | 1.93 |
| widen-column-60 | nocopy | success | INSERT | after | 112 | False | 112 | 0 | 1.69 | 1.59 | 2.16 | 5.06 | 6.93 |
| widen-column-60 | nocopy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.60 | 1.51 | 2.26 | 3.78 | 4.64 |
| widen-column-60 | nocopy | success | INSERT | during | 2 | True | 2 | 0 | 8.55 | 8.55 | 9.28 | 9.35 | 9.36 |
| widen-column-60 | nocopy | success | UPDATE | after | 114 | False | 114 | 0 | 0.73 | 0.71 | 1.29 | 1.62 | 1.76 |
| widen-column-60 | nocopy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.65 | 0.58 | 1.13 | 2.37 | 3.54 |
| widen-column-60 | instant | success | DELETE | after | 112 | False | 112 | 0 | 0.72 | 0.65 | 1.13 | 1.52 | 3.03 |
| widen-column-60 | instant | success | DELETE | baseline | 98 | False | 98 | 0 | 0.64 | 0.60 | 1.00 | 1.35 | 1.50 |
| widen-column-60 | instant | success | INSERT | after | 112 | False | 112 | 0 | 1.92 | 1.57 | 2.17 | 15.43 | 17.36 |
| widen-column-60 | instant | success | INSERT | baseline | 198 | False | 198 | 0 | 1.53 | 1.50 | 1.98 | 2.43 | 3.82 |
| widen-column-60 | instant | success | UPDATE | after | 112 | False | 112 | 0 | 0.69 | 0.69 | 1.10 | 1.42 | 1.73 |
| widen-column-60 | instant | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.57 | 0.54 | 0.95 | 1.14 | 2.28 |
| widen-column-100 | default | success | DELETE | after | 114 | False | 114 | 0 | 0.64 | 0.61 | 1.00 | 1.19 | 1.28 |
| widen-column-100 | default | success | DELETE | baseline | 98 | False | 98 | 0 | 0.61 | 0.58 | 0.88 | 1.06 | 1.23 |
| widen-column-100 | default | success | INSERT | after | 114 | False | 114 | 0 | 1.57 | 1.51 | 2.05 | 3.61 | 3.84 |
| widen-column-100 | default | success | INSERT | baseline | 198 | False | 198 | 0 | 1.47 | 1.45 | 1.91 | 2.23 | 2.41 |
| widen-column-100 | default | success | UPDATE | after | 114 | False | 114 | 0 | 0.71 | 0.67 | 1.13 | 3.76 | 4.14 |
| widen-column-100 | default | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.59 | 0.54 | 1.08 | 1.45 | 1.79 |
| widen-column-100 | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.75 | 0.61 | 1.51 | 2.51 | 5.92 |
| widen-column-100 | blocking | success | DELETE | baseline | 98 | False | 98 | 0 | 0.60 | 0.58 | 0.92 | 1.07 | 1.17 |
| widen-column-100 | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.52 | 1.47 | 1.90 | 3.98 | 6.46 |
| widen-column-100 | blocking | success | INSERT | baseline | 198 | False | 198 | 0 | 1.54 | 1.46 | 2.27 | 3.44 | 5.64 |
| widen-column-100 | blocking | success | INSERT | during | 2 | True | 2 | 0 | 2715.40 | 2715.40 | 2715.86 | 2715.90 | 2715.91 |
| widen-column-100 | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.68 | 0.64 | 1.16 | 2.71 | 2.95 |
| widen-column-100 | blocking | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.59 | 0.58 | 0.96 | 1.22 | 2.96 |
| widen-column-100 | copy | success | DELETE | after | 112 | False | 112 | 0 | 0.74 | 0.71 | 1.02 | 1.38 | 1.78 |
| widen-column-100 | copy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.62 | 0.59 | 1.01 | 1.49 | 1.70 |
| widen-column-100 | copy | success | DELETE | during | 60 | False | 60 | 0 | 8.17 | 1.01 | 49.55 | 101.87 | 106.89 |
| widen-column-100 | copy | success | INSERT | after | 112 | False | 112 | 0 | 1.99 | 1.60 | 2.70 | 7.52 | 29.79 |
| widen-column-100 | copy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.50 | 1.40 | 2.11 | 3.43 | 4.03 |
| widen-column-100 | copy | success | INSERT | during | 60 | False | 60 | 0 | 15.26 | 6.37 | 56.62 | 90.28 | 104.14 |
| widen-column-100 | copy | success | UPDATE | after | 112 | False | 112 | 0 | 0.92 | 0.77 | 1.05 | 1.52 | 22.95 |
| widen-column-100 | copy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.59 | 0.57 | 0.98 | 1.57 | 3.42 |
| widen-column-100 | copy | success | UPDATE | during | 60 | False | 60 | 0 | 4.03 | 1.07 | 6.82 | 69.87 | 76.94 |
| widen-column-100 | copy-shared | success | DELETE | after | 114 | False | 114 | 0 | 0.62 | 0.56 | 1.04 | 1.52 | 1.75 |
| widen-column-100 | copy-shared | success | DELETE | baseline | 98 | False | 98 | 0 | 0.56 | 0.53 | 0.88 | 1.05 | 1.55 |
| widen-column-100 | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.43 | 1.32 | 1.84 | 4.28 | 6.32 |
| widen-column-100 | copy-shared | success | INSERT | baseline | 198 | False | 198 | 0 | 1.55 | 1.30 | 1.80 | 2.95 | 23.67 |
| widen-column-100 | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 2477.74 | 2477.74 | 2478.16 | 2478.20 | 2478.21 |
| widen-column-100 | copy-shared | success | UPDATE | after | 114 | False | 114 | 0 | 0.66 | 0.64 | 1.05 | 1.70 | 4.49 |
| widen-column-100 | copy-shared | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.57 | 0.52 | 0.91 | 1.62 | 4.70 |
| widen-column-100 | inplace | success | DELETE | after | 114 | False | 114 | 0 | 0.65 | 0.61 | 0.97 | 1.39 | 1.41 |
| widen-column-100 | inplace | success | DELETE | baseline | 98 | False | 98 | 0 | 0.63 | 0.56 | 0.94 | 2.66 | 2.87 |
| widen-column-100 | inplace | success | INSERT | after | 114 | False | 114 | 0 | 1.44 | 1.37 | 2.23 | 3.64 | 3.83 |
| widen-column-100 | inplace | success | INSERT | baseline | 198 | False | 198 | 0 | 1.42 | 1.35 | 1.90 | 3.03 | 3.80 |
| widen-column-100 | inplace | success | UPDATE | after | 114 | False | 114 | 0 | 0.65 | 0.59 | 1.11 | 1.84 | 2.52 |
| widen-column-100 | inplace | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.61 | 0.57 | 1.04 | 2.33 | 3.39 |
| widen-column-100 | nocopy | success | DELETE | after | 116 | False | 116 | 0 | 0.58 | 0.55 | 0.91 | 1.26 | 1.31 |
| widen-column-100 | nocopy | success | DELETE | baseline | 98 | False | 98 | 0 | 0.63 | 0.57 | 0.97 | 1.57 | 2.63 |
| widen-column-100 | nocopy | success | INSERT | after | 115 | False | 115 | 0 | 1.35 | 1.34 | 1.69 | 1.95 | 2.24 |
| widen-column-100 | nocopy | success | INSERT | baseline | 198 | False | 198 | 0 | 1.52 | 1.42 | 2.13 | 4.37 | 5.10 |
| widen-column-100 | nocopy | success | INSERT | during | 1 | True | 1 | 0 | 2.27 | 2.27 | 2.27 | 2.27 | 2.27 |
| widen-column-100 | nocopy | success | UPDATE | after | 116 | False | 116 | 0 | 0.66 | 0.61 | 1.07 | 2.70 | 3.41 |
| widen-column-100 | nocopy | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.60 | 0.56 | 1.00 | 1.84 | 2.42 |
| widen-column-100 | instant | success | DELETE | after | 114 | False | 114 | 0 | 0.61 | 0.55 | 1.02 | 2.10 | 2.83 |
| widen-column-100 | instant | success | DELETE | baseline | 98 | False | 98 | 0 | 0.64 | 0.55 | 1.28 | 1.51 | 2.11 |
| widen-column-100 | instant | success | INSERT | after | 114 | False | 114 | 0 | 1.43 | 1.40 | 1.92 | 2.11 | 2.62 |
| widen-column-100 | instant | success | INSERT | baseline | 198 | False | 198 | 0 | 1.43 | 1.34 | 1.98 | 3.97 | 5.11 |
| widen-column-100 | instant | success | UPDATE | after | 114 | False | 114 | 0 | 0.62 | 0.64 | 1.10 | 1.33 | 1.80 |
| widen-column-100 | instant | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.56 | 0.54 | 0.98 | 1.40 | 2.06 |
| widen-column-rebuild | default | success | DELETE | after | 114 | False | 114 | 0 | 0.66 | 0.58 | 1.10 | 1.87 | 2.13 |
| widen-column-rebuild | default | success | DELETE | baseline | 96 | False | 96 | 0 | 0.75 | 0.67 | 1.23 | 2.52 | 2.81 |
| widen-column-rebuild | default | success | DELETE | during | 68 | False | 68 | 0 | 5.20 | 1.22 | 30.44 | 48.82 | 50.60 |
| widen-column-rebuild | default | success | INSERT | after | 114 | False | 114 | 0 | 1.41 | 1.36 | 1.96 | 2.42 | 2.73 |
| widen-column-rebuild | default | success | INSERT | baseline | 196 | False | 196 | 0 | 1.62 | 1.50 | 2.31 | 5.09 | 7.11 |
| widen-column-rebuild | default | success | INSERT | during | 68 | False | 68 | 0 | 14.64 | 6.52 | 51.00 | 77.61 | 80.38 |
| widen-column-rebuild | default | success | UPDATE | after | 114 | False | 114 | 0 | 0.66 | 0.65 | 1.06 | 1.65 | 1.80 |
| widen-column-rebuild | default | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.63 | 0.61 | 1.06 | 1.30 | 3.41 |
| widen-column-rebuild | default | success | UPDATE | during | 68 | False | 68 | 0 | 3.11 | 1.13 | 8.67 | 42.58 | 51.41 |
| widen-column-rebuild | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.62 | 0.56 | 0.92 | 1.11 | 4.44 |
| widen-column-rebuild | blocking | success | DELETE | baseline | 98 | False | 98 | 0 | 0.59 | 0.57 | 0.90 | 1.03 | 1.27 |
| widen-column-rebuild | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.76 | 1.30 | 1.78 | 22.24 | 24.81 |
| widen-column-rebuild | blocking | success | INSERT | baseline | 198 | False | 198 | 0 | 1.38 | 1.29 | 1.92 | 3.87 | 4.08 |
| widen-column-rebuild | blocking | success | INSERT | during | 2 | True | 2 | 0 | 2499.71 | 2499.71 | 2500.12 | 2500.15 | 2500.16 |
| widen-column-rebuild | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.61 | 0.60 | 0.92 | 1.27 | 4.66 |
| widen-column-rebuild | blocking | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.54 | 0.53 | 0.93 | 1.33 | 1.48 |
| widen-column-rebuild | copy | success | DELETE | after | 114 | False | 114 | 0 | 0.60 | 0.56 | 0.91 | 1.22 | 1.25 |
| widen-column-rebuild | copy | success | DELETE | baseline | 100 | False | 100 | 0 | 0.63 | 0.55 | 0.93 | 2.15 | 3.16 |
| widen-column-rebuild | copy | success | DELETE | during | 60 | False | 60 | 0 | 5.90 | 0.99 | 43.59 | 48.55 | 51.48 |
| widen-column-rebuild | copy | success | INSERT | after | 114 | False | 114 | 0 | 1.75 | 1.34 | 2.24 | 20.76 | 23.69 |
| widen-column-rebuild | copy | success | INSERT | baseline | 200 | False | 200 | 0 | 1.39 | 1.33 | 1.86 | 2.64 | 4.31 |
| widen-column-rebuild | copy | success | INSERT | during | 60 | False | 60 | 0 | 15.28 | 5.53 | 53.99 | 85.45 | 86.00 |
| widen-column-rebuild | copy | success | UPDATE | after | 114 | False | 114 | 0 | 0.65 | 0.62 | 1.22 | 1.51 | 1.62 |
| widen-column-rebuild | copy | success | UPDATE | baseline | 200 | False | 200 | 0 | 0.61 | 0.55 | 1.10 | 1.91 | 3.59 |
| widen-column-rebuild | copy | success | UPDATE | during | 60 | False | 60 | 0 | 2.50 | 0.95 | 5.92 | 35.83 | 49.84 |
| widen-column-rebuild | copy-shared | success | DELETE | after | 114 | False | 114 | 0 | 0.94 | 0.61 | 1.21 | 2.93 | 29.39 |
| widen-column-rebuild | copy-shared | success | DELETE | baseline | 98 | False | 98 | 0 | 0.61 | 0.58 | 1.02 | 1.24 | 1.25 |
| widen-column-rebuild | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.81 | 1.39 | 2.02 | 6.95 | 36.43 |
| widen-column-rebuild | copy-shared | success | INSERT | baseline | 198 | False | 198 | 0 | 1.44 | 1.38 | 2.21 | 3.26 | 4.74 |
| widen-column-rebuild | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 2595.73 | 2595.73 | 2598.09 | 2598.30 | 2598.35 |
| widen-column-rebuild | copy-shared | success | UPDATE | after | 114 | False | 114 | 0 | 0.74 | 0.65 | 1.51 | 3.33 | 3.58 |
| widen-column-rebuild | copy-shared | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.63 | 0.59 | 1.06 | 2.84 | 4.22 |
| widen-column-rebuild | inplace | failure | DELETE | after | 114 | False | 114 | 0 | 0.62 | 0.57 | 0.89 | 1.18 | 2.71 |
| widen-column-rebuild | inplace | failure | DELETE | baseline | 96 | False | 96 | 0 | 0.76 | 0.63 | 1.08 | 4.09 | 6.14 |
| widen-column-rebuild | inplace | failure | DELETE | during | 2 | True | 2 | 0 | 1.57 | 1.57 | 1.71 | 1.72 | 1.72 |
| widen-column-rebuild | inplace | failure | INSERT | after | 114 | False | 114 | 0 | 1.45 | 1.41 | 1.80 | 3.05 | 3.58 |
| widen-column-rebuild | inplace | failure | INSERT | baseline | 196 | False | 196 | 0 | 1.49 | 1.44 | 1.92 | 3.35 | 3.92 |
| widen-column-rebuild | inplace | failure | INSERT | during | 2 | True | 2 | 0 | 1.82 | 1.82 | 1.84 | 1.84 | 1.84 |
| widen-column-rebuild | inplace | failure | UPDATE | after | 114 | False | 114 | 0 | 0.62 | 0.60 | 1.01 | 1.12 | 2.78 |
| widen-column-rebuild | inplace | failure | UPDATE | baseline | 196 | False | 196 | 0 | 0.59 | 0.59 | 0.98 | 1.26 | 1.37 |
| widen-column-rebuild | inplace | failure | UPDATE | during | 2 | True | 2 | 0 | 0.90 | 0.90 | 1.40 | 1.44 | 1.45 |
| widen-column-rebuild | nocopy | failure | DELETE | after | 112 | False | 112 | 0 | 0.72 | 0.65 | 0.98 | 3.95 | 4.36 |
| widen-column-rebuild | nocopy | failure | DELETE | baseline | 98 | False | 98 | 0 | 0.62 | 0.58 | 0.99 | 1.19 | 1.39 |
| widen-column-rebuild | nocopy | failure | INSERT | after | 112 | False | 112 | 0 | 2.02 | 1.44 | 2.79 | 24.63 | 27.30 |
| widen-column-rebuild | nocopy | failure | INSERT | baseline | 198 | False | 198 | 0 | 1.47 | 1.42 | 1.93 | 3.18 | 3.97 |
| widen-column-rebuild | nocopy | failure | UPDATE | after | 112 | False | 112 | 0 | 0.68 | 0.66 | 1.20 | 2.95 | 3.50 |
| widen-column-rebuild | nocopy | failure | UPDATE | baseline | 198 | False | 198 | 0 | 0.59 | 0.54 | 1.13 | 1.51 | 2.02 |
| widen-column-rebuild | instant | failure | DELETE | after | 114 | False | 114 | 0 | 0.63 | 0.60 | 0.96 | 1.25 | 1.49 |
| widen-column-rebuild | instant | failure | DELETE | baseline | 98 | False | 98 | 0 | 0.60 | 0.55 | 0.96 | 1.26 | 3.40 |
| widen-column-rebuild | instant | failure | INSERT | after | 114 | False | 114 | 0 | 1.40 | 1.40 | 1.74 | 1.84 | 2.13 |
| widen-column-rebuild | instant | failure | INSERT | baseline | 198 | False | 198 | 0 | 1.46 | 1.41 | 2.04 | 3.79 | 4.29 |
| widen-column-rebuild | instant | failure | UPDATE | after | 114 | False | 114 | 0 | 0.61 | 0.62 | 0.98 | 1.15 | 1.47 |
| widen-column-rebuild | instant | failure | UPDATE | baseline | 198 | False | 198 | 0 | 0.60 | 0.55 | 1.04 | 1.65 | 3.94 |
| add-fk | default | success | DELETE | after | 114 | False | 114 | 0 | 0.71 | 0.68 | 1.13 | 1.28 | 1.29 |
| add-fk | default | success | DELETE | baseline | 98 | False | 98 | 0 | 0.56 | 0.55 | 0.85 | 0.94 | 1.07 |
| add-fk | default | success | DELETE | during | 234 | False | 234 | 0 | 0.87 | 0.83 | 1.56 | 1.72 | 2.04 |
| add-fk | default | success | INSERT | after | 114 | False | 114 | 0 | 1.78 | 1.57 | 3.53 | 4.91 | 4.96 |
| add-fk | default | success | INSERT | baseline | 198 | False | 198 | 0 | 1.59 | 1.41 | 3.23 | 4.38 | 5.51 |
| add-fk | default | success | INSERT | during | 234 | False | 234 | 0 | 2.40 | 2.17 | 3.21 | 8.12 | 8.32 |
| add-fk | default | success | UPDATE | after | 114 | False | 114 | 0 | 0.69 | 0.68 | 1.16 | 2.95 | 3.39 |
| add-fk | default | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.58 | 0.52 | 1.04 | 1.59 | 2.42 |
| add-fk | default | success | UPDATE | during | 234 | False | 234 | 0 | 0.92 | 0.88 | 1.66 | 2.34 | 2.67 |
| add-fk | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.68 | 0.64 | 1.14 | 1.35 | 2.50 |
| add-fk | blocking | success | DELETE | baseline | 98 | False | 98 | 0 | 0.61 | 0.58 | 0.88 | 0.95 | 0.96 |
| add-fk | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.65 | 1.51 | 3.41 | 4.71 | 5.06 |
| add-fk | blocking | success | INSERT | baseline | 198 | False | 198 | 0 | 1.55 | 1.47 | 2.09 | 3.28 | 4.78 |
| add-fk | blocking | success | INSERT | during | 2 | True | 2 | 0 | 6549.04 | 6549.04 | 6550.98 | 6551.15 | 6551.19 |
| add-fk | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.72 | 0.69 | 1.00 | 1.83 | 7.12 |
| add-fk | blocking | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.58 | 0.58 | 1.00 | 1.20 | 1.55 |
| add-fk | copy | success | DELETE | after | 114 | False | 114 | 0 | 0.65 | 0.58 | 1.07 | 1.44 | 1.74 |
| add-fk | copy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.75 | 0.67 | 1.22 | 2.17 | 2.25 |
| add-fk | copy | success | DELETE | during | 264 | False | 264 | 0 | 0.95 | 0.81 | 1.83 | 3.22 | 5.27 |
| add-fk | copy | success | INSERT | after | 114 | False | 114 | 0 | 1.74 | 1.53 | 3.05 | 5.38 | 7.30 |
| add-fk | copy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.61 | 1.54 | 2.54 | 3.36 | 4.13 |
| add-fk | copy | success | INSERT | during | 264 | False | 264 | 0 | 2.41 | 2.17 | 4.76 | 6.06 | 7.14 |
| add-fk | copy | success | UPDATE | after | 114 | False | 114 | 0 | 0.69 | 0.64 | 1.20 | 2.19 | 2.36 |
| add-fk | copy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.67 | 0.65 | 1.16 | 1.43 | 1.69 |
| add-fk | copy | success | UPDATE | during | 264 | False | 264 | 0 | 0.97 | 0.93 | 1.91 | 2.77 | 6.19 |
| add-fk | copy-shared | success | DELETE | after | 113 | False | 113 | 0 | 0.66 | 0.60 | 0.97 | 1.82 | 3.29 |
| add-fk | copy-shared | success | DELETE | baseline | 96 | False | 96 | 0 | 0.73 | 0.62 | 1.21 | 3.35 | 3.68 |
| add-fk | copy-shared | success | DELETE | during | 1 | True | 1 | 0 | 7193.44 | 7193.44 | 7193.44 | 7193.44 | 7193.44 |
| add-fk | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.58 | 1.50 | 2.21 | 3.11 | 3.43 |
| add-fk | copy-shared | success | INSERT | baseline | 196 | False | 196 | 0 | 1.66 | 1.44 | 3.32 | 4.53 | 4.54 |
| add-fk | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 1.48 | 1.48 | 1.65 | 1.67 | 1.67 |
| add-fk | copy-shared | success | UPDATE | after | 112 | False | 112 | 0 | 0.61 | 0.62 | 1.02 | 1.08 | 1.40 |
| add-fk | copy-shared | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.67 | 0.60 | 1.17 | 2.60 | 4.03 |
| add-fk | copy-shared | success | UPDATE | during | 2 | True | 2 | 0 | 3596.85 | 3596.85 | 6833.21 | 7120.89 | 7192.81 |
| add-fk | inplace | failure | DELETE | after | 114 | False | 114 | 0 | 0.59 | 0.55 | 0.89 | 1.40 | 1.48 |
| add-fk | inplace | failure | DELETE | baseline | 98 | False | 98 | 0 | 0.70 | 0.64 | 1.13 | 1.78 | 2.63 |
| add-fk | inplace | failure | INSERT | after | 114 | False | 114 | 0 | 1.63 | 1.44 | 3.27 | 4.06 | 5.79 |
| add-fk | inplace | failure | INSERT | baseline | 198 | False | 198 | 0 | 1.57 | 1.49 | 2.37 | 3.36 | 3.83 |
| add-fk | inplace | failure | UPDATE | after | 114 | False | 114 | 0 | 0.63 | 0.59 | 1.08 | 1.43 | 1.56 |
| add-fk | inplace | failure | UPDATE | baseline | 198 | False | 198 | 0 | 0.61 | 0.54 | 1.17 | 2.02 | 2.42 |
| add-fk | nocopy | failure | DELETE | after | 114 | False | 114 | 0 | 0.61 | 0.57 | 0.87 | 1.82 | 2.27 |
| add-fk | nocopy | failure | DELETE | baseline | 96 | False | 96 | 0 | 0.60 | 0.58 | 0.87 | 1.05 | 1.53 |
| add-fk | nocopy | failure | INSERT | after | 114 | False | 114 | 0 | 1.57 | 1.37 | 2.37 | 8.96 | 9.81 |
| add-fk | nocopy | failure | INSERT | baseline | 196 | False | 196 | 0 | 1.61 | 1.45 | 3.05 | 4.23 | 4.40 |
| add-fk | nocopy | failure | UPDATE | after | 114 | False | 114 | 0 | 0.61 | 0.58 | 1.03 | 1.79 | 2.42 |
| add-fk | nocopy | failure | UPDATE | baseline | 196 | False | 196 | 0 | 0.59 | 0.54 | 1.04 | 1.50 | 2.20 |
| add-fk | instant | failure | DELETE | after | 114 | False | 114 | 0 | 0.66 | 0.62 | 1.06 | 1.95 | 2.05 |
| add-fk | instant | failure | DELETE | baseline | 96 | False | 96 | 0 | 0.67 | 0.61 | 1.08 | 1.52 | 1.94 |
| add-fk | instant | failure | INSERT | after | 114 | False | 114 | 0 | 2.35 | 1.49 | 6.04 | 25.94 | 28.87 |
| add-fk | instant | failure | INSERT | baseline | 196 | False | 196 | 0 | 1.59 | 1.48 | 2.78 | 3.38 | 4.11 |
| add-fk | instant | failure | UPDATE | after | 114 | False | 114 | 0 | 0.68 | 0.67 | 1.14 | 1.39 | 2.65 |
| add-fk | instant | failure | UPDATE | baseline | 196 | False | 196 | 0 | 0.61 | 0.57 | 1.04 | 1.46 | 3.61 |
| add-fk-fkchecks-off | default | success | DELETE | after | 112 | False | 112 | 0 | 0.79 | 0.74 | 1.30 | 1.62 | 2.32 |
| add-fk-fkchecks-off | default | success | DELETE | baseline | 98 | False | 98 | 0 | 0.61 | 0.58 | 0.91 | 1.05 | 1.11 |
| add-fk-fkchecks-off | default | success | DELETE | during | 30 | False | 30 | 0 | 1.55 | 0.84 | 5.95 | 7.44 | 7.82 |
| add-fk-fkchecks-off | default | success | INSERT | after | 112 | False | 112 | 0 | 1.88 | 1.77 | 3.42 | 4.10 | 4.70 |
| add-fk-fkchecks-off | default | success | INSERT | baseline | 198 | False | 198 | 0 | 1.63 | 1.49 | 3.27 | 4.14 | 4.43 |
| add-fk-fkchecks-off | default | success | INSERT | during | 30 | False | 30 | 0 | 4.62 | 3.37 | 9.97 | 11.95 | 12.40 |
| add-fk-fkchecks-off | default | success | UPDATE | after | 112 | False | 112 | 0 | 0.73 | 0.72 | 1.22 | 1.35 | 1.94 |
| add-fk-fkchecks-off | default | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.62 | 0.59 | 1.13 | 1.95 | 2.48 |
| add-fk-fkchecks-off | default | success | UPDATE | during | 30 | False | 30 | 0 | 1.19 | 0.94 | 2.26 | 5.52 | 6.79 |
| add-fk-fkchecks-off | blocking | success | DELETE | after | 114 | False | 114 | 0 | 0.63 | 0.61 | 0.98 | 1.24 | 1.27 |
| add-fk-fkchecks-off | blocking | success | DELETE | baseline | 98 | False | 98 | 0 | 0.70 | 0.63 | 1.10 | 2.17 | 2.90 |
| add-fk-fkchecks-off | blocking | success | INSERT | after | 112 | False | 112 | 0 | 1.77 | 1.56 | 3.29 | 6.43 | 7.14 |
| add-fk-fkchecks-off | blocking | success | INSERT | baseline | 198 | False | 198 | 0 | 1.58 | 1.45 | 2.96 | 3.68 | 3.81 |
| add-fk-fkchecks-off | blocking | success | INSERT | during | 2 | True | 2 | 0 | 2321.17 | 2321.17 | 2321.42 | 2321.44 | 2321.45 |
| add-fk-fkchecks-off | blocking | success | UPDATE | after | 114 | False | 114 | 0 | 0.69 | 0.63 | 1.41 | 2.16 | 2.24 |
| add-fk-fkchecks-off | blocking | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.59 | 0.56 | 0.98 | 1.28 | 1.34 |
| add-fk-fkchecks-off | copy | success | DELETE | after | 112 | False | 112 | 0 | 0.70 | 0.64 | 1.02 | 2.30 | 2.92 |
| add-fk-fkchecks-off | copy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.62 | 0.57 | 1.12 | 1.30 | 1.65 |
| add-fk-fkchecks-off | copy | success | DELETE | during | 67 | False | 67 | 0 | 2.09 | 0.94 | 8.39 | 12.95 | 13.05 |
| add-fk-fkchecks-off | copy | success | INSERT | after | 112 | False | 112 | 0 | 1.67 | 1.64 | 2.35 | 4.08 | 4.49 |
| add-fk-fkchecks-off | copy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.65 | 1.43 | 2.99 | 4.90 | 12.15 |
| add-fk-fkchecks-off | copy | success | INSERT | during | 67 | False | 67 | 0 | 7.92 | 4.02 | 27.66 | 36.84 | 38.93 |
| add-fk-fkchecks-off | copy | success | UPDATE | after | 112 | False | 112 | 0 | 0.66 | 0.62 | 1.11 | 2.47 | 2.58 |
| add-fk-fkchecks-off | copy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.57 | 0.53 | 1.07 | 1.56 | 1.68 |
| add-fk-fkchecks-off | copy | success | UPDATE | during | 67 | False | 67 | 0 | 2.69 | 1.00 | 15.48 | 23.43 | 25.89 |
| add-fk-fkchecks-off | copy-shared | success | DELETE | after | 114 | False | 114 | 0 | 0.69 | 0.63 | 1.02 | 1.46 | 2.73 |
| add-fk-fkchecks-off | copy-shared | success | DELETE | baseline | 96 | False | 96 | 0 | 0.76 | 0.71 | 1.12 | 1.24 | 1.34 |
| add-fk-fkchecks-off | copy-shared | success | INSERT | after | 112 | False | 112 | 0 | 1.65 | 1.60 | 2.02 | 4.31 | 4.71 |
| add-fk-fkchecks-off | copy-shared | success | INSERT | baseline | 196 | False | 196 | 0 | 1.88 | 1.66 | 3.50 | 4.85 | 12.13 |
| add-fk-fkchecks-off | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 2605.63 | 2605.63 | 2606.15 | 2606.20 | 2606.21 |
| add-fk-fkchecks-off | copy-shared | success | UPDATE | after | 114 | False | 114 | 0 | 0.70 | 0.66 | 1.14 | 2.65 | 4.37 |
| add-fk-fkchecks-off | copy-shared | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.66 | 0.63 | 1.36 | 1.80 | 2.10 |
| add-fk-fkchecks-off | inplace | success | DELETE | after | 114 | False | 114 | 0 | 0.69 | 0.63 | 1.16 | 1.71 | 2.41 |
| add-fk-fkchecks-off | inplace | success | DELETE | baseline | 98 | False | 98 | 0 | 0.62 | 0.55 | 1.07 | 1.36 | 2.91 |
| add-fk-fkchecks-off | inplace | success | DELETE | during | 26 | True | 26 | 0 | 1.38 | 1.08 | 3.43 | 4.64 | 5.00 |
| add-fk-fkchecks-off | inplace | success | INSERT | after | 112 | False | 112 | 0 | 1.78 | 1.72 | 2.83 | 3.45 | 3.83 |
| add-fk-fkchecks-off | inplace | success | INSERT | baseline | 198 | False | 198 | 0 | 1.55 | 1.42 | 2.61 | 3.42 | 4.49 |
| add-fk-fkchecks-off | inplace | success | INSERT | during | 28 | True | 28 | 0 | 5.24 | 2.87 | 13.88 | 15.94 | 16.62 |
| add-fk-fkchecks-off | inplace | success | UPDATE | after | 112 | False | 112 | 0 | 0.70 | 0.65 | 1.32 | 1.66 | 1.73 |
| add-fk-fkchecks-off | inplace | success | UPDATE | baseline | 198 | False | 198 | 0 | 0.58 | 0.57 | 1.01 | 1.17 | 2.74 |
| add-fk-fkchecks-off | inplace | success | UPDATE | during | 28 | True | 28 | 0 | 1.70 | 1.06 | 6.39 | 7.49 | 7.90 |
| add-fk-fkchecks-off | nocopy | success | DELETE | after | 114 | False | 114 | 0 | 0.75 | 0.63 | 1.33 | 2.57 | 2.95 |
| add-fk-fkchecks-off | nocopy | success | DELETE | baseline | 96 | False | 96 | 0 | 0.73 | 0.70 | 1.10 | 1.21 | 1.68 |
| add-fk-fkchecks-off | nocopy | success | DELETE | during | 32 | False | 32 | 0 | 1.12 | 1.03 | 1.87 | 2.15 | 2.17 |
| add-fk-fkchecks-off | nocopy | success | INSERT | after | 114 | False | 114 | 0 | 1.91 | 1.69 | 3.47 | 6.85 | 7.97 |
| add-fk-fkchecks-off | nocopy | success | INSERT | baseline | 196 | False | 196 | 0 | 1.72 | 1.53 | 3.20 | 4.36 | 6.25 |
| add-fk-fkchecks-off | nocopy | success | INSERT | during | 32 | False | 32 | 0 | 4.68 | 3.50 | 9.04 | 9.68 | 9.92 |
| add-fk-fkchecks-off | nocopy | success | UPDATE | after | 114 | False | 114 | 0 | 0.72 | 0.68 | 1.19 | 3.57 | 5.32 |
| add-fk-fkchecks-off | nocopy | success | UPDATE | baseline | 196 | False | 196 | 0 | 0.72 | 0.64 | 1.33 | 2.78 | 4.79 |
| add-fk-fkchecks-off | nocopy | success | UPDATE | during | 32 | False | 32 | 0 | 1.26 | 1.22 | 2.61 | 3.53 | 3.84 |
| add-fk-fkchecks-off | instant | failure | DELETE | after | 114 | False | 114 | 0 | 0.74 | 0.70 | 1.26 | 1.70 | 1.73 |
| add-fk-fkchecks-off | instant | failure | DELETE | baseline | 96 | False | 96 | 0 | 0.72 | 0.68 | 1.17 | 1.96 | 2.25 |
| add-fk-fkchecks-off | instant | failure | INSERT | after | 114 | False | 114 | 0 | 1.73 | 1.56 | 3.41 | 4.65 | 5.57 |
| add-fk-fkchecks-off | instant | failure | INSERT | baseline | 196 | False | 196 | 0 | 1.68 | 1.56 | 3.16 | 3.92 | 5.59 |
| add-fk-fkchecks-off | instant | failure | UPDATE | after | 114 | False | 114 | 0 | 0.75 | 0.70 | 1.48 | 1.87 | 1.92 |
| add-fk-fkchecks-off | instant | failure | UPDATE | baseline | 196 | False | 196 | 0 | 0.66 | 0.61 | 1.18 | 1.39 | 2.41 |


## Figures

- fig_alter_duration.png
- fig_workload_p95.png
- fig_latency_distribution.png
- fig_workload_errors.png: not generated (no applicable data)
