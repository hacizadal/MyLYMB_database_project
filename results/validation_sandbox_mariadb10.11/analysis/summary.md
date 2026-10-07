# Analysis of validation_sandbox_mariadb10.11

- Server: `10.11.14-MariaDB-0ubuntu0.24.04.1`
- Dataset rows (target table): 200000
- ALTER runs: 42  (success: 28, failure: 14)

## ALTER duration and outcome

| change | algorithm | runs | successes | failures | mean_s | median_s | min_s | max_s | first_error |
|---|---|---|---|---|---|---|---|---|---|
| change-type | default | 1 | 1 | 0 | 0.854 | 0.854 | 0.854 | 0.854 |  |
| change-type | blocking | 1 | 1 | 0 | 0.883 | 0.883 | 0.883 | 0.883 |  |
| change-type | copy | 1 | 0 | 1 |  |  |  |  | (1846, 'LOCK=NONE is not supported. Reason: COPY algorithm requires a lock. Try LOCK=SHARED') |
| change-type | copy-shared | 1 | 1 | 0 | 0.855 | 0.855 | 0.855 | 0.855 |  |
| change-type | inplace | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INPLACE is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| change-type | nocopy | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=NOCOPY is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| change-type | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: Cannot change column type. Try ALGORITHM=COPY') |
| add-index | default | 1 | 1 | 0 | 0.285 | 0.285 | 0.285 | 0.285 |  |
| add-index | blocking | 1 | 1 | 0 | 0.958 | 0.958 | 0.958 | 0.958 |  |
| add-index | copy | 1 | 0 | 1 |  |  |  |  | (1846, 'LOCK=NONE is not supported. Reason: COPY algorithm requires a lock. Try LOCK=SHARED') |
| add-index | copy-shared | 1 | 1 | 0 | 0.941 | 0.941 | 0.941 | 0.941 |  |
| add-index | inplace | 1 | 1 | 0 | 0.304 | 0.304 | 0.304 | 0.304 |  |
| add-index | nocopy | 1 | 1 | 0 | 0.266 | 0.266 | 0.266 | 0.266 |  |
| add-index | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: ADD INDEX. Try ALGORITHM=NOCOPY') |
| widen-column-60 | default | 1 | 1 | 0 | 0.043 | 0.043 | 0.043 | 0.043 |  |
| widen-column-60 | blocking | 1 | 1 | 0 | 0.769 | 0.769 | 0.769 | 0.769 |  |
| widen-column-60 | copy | 1 | 0 | 1 |  |  |  |  | (1846, 'LOCK=NONE is not supported. Reason: COPY algorithm requires a lock. Try LOCK=SHARED') |
| widen-column-60 | copy-shared | 1 | 1 | 0 | 0.727 | 0.727 | 0.727 | 0.727 |  |
| widen-column-60 | inplace | 1 | 1 | 0 | 0.044 | 0.044 | 0.044 | 0.044 |  |
| widen-column-60 | nocopy | 1 | 1 | 0 | 0.041 | 0.041 | 0.041 | 0.041 |  |
| widen-column-60 | instant | 1 | 1 | 0 | 0.050 | 0.050 | 0.050 | 0.050 |  |
| widen-column-100 | default | 1 | 1 | 0 | 0.052 | 0.052 | 0.052 | 0.052 |  |
| widen-column-100 | blocking | 1 | 1 | 0 | 0.769 | 0.769 | 0.769 | 0.769 |  |
| widen-column-100 | copy | 1 | 0 | 1 |  |  |  |  | (1846, 'LOCK=NONE is not supported. Reason: COPY algorithm requires a lock. Try LOCK=SHARED') |
| widen-column-100 | copy-shared | 1 | 1 | 0 | 0.965 | 0.965 | 0.965 | 0.965 |  |
| widen-column-100 | inplace | 1 | 1 | 0 | 0.043 | 0.043 | 0.043 | 0.043 |  |
| widen-column-100 | nocopy | 1 | 1 | 0 | 0.043 | 0.043 | 0.043 | 0.043 |  |
| widen-column-100 | instant | 1 | 1 | 0 | 0.047 | 0.047 | 0.047 | 0.047 |  |
| add-fk | default | 1 | 1 | 0 | 1.924 | 1.924 | 1.924 | 1.924 |  |
| add-fk | blocking | 1 | 1 | 0 | 1.715 | 1.715 | 1.715 | 1.715 |  |
| add-fk | copy | 1 | 0 | 1 |  |  |  |  | (1846, 'LOCK=NONE is not supported. Reason: COPY algorithm requires a lock. Try LOCK=SHARED') |
| add-fk | copy-shared | 1 | 1 | 0 | 1.918 | 1.918 | 1.918 | 1.918 |  |
| add-fk | inplace | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INPLACE is not supported. Reason: Adding foreign keys needs foreign_key_checks=OFF. Try ALGORITHM=COPY') |
| add-fk | nocopy | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=NOCOPY is not supported. Reason: Adding foreign keys needs foreign_key_checks=OFF. Try ALGORITHM=COPY') |
| add-fk | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: Adding foreign keys needs foreign_key_checks=OFF. Try ALGORITHM=COPY') |
| add-fk-fkchecks-off | default | 1 | 1 | 0 | 0.347 | 0.347 | 0.347 | 0.347 |  |
| add-fk-fkchecks-off | blocking | 1 | 1 | 0 | 0.760 | 0.760 | 0.760 | 0.760 |  |
| add-fk-fkchecks-off | copy | 1 | 0 | 1 |  |  |  |  | (1846, 'LOCK=NONE is not supported. Reason: COPY algorithm requires a lock. Try LOCK=SHARED') |
| add-fk-fkchecks-off | copy-shared | 1 | 1 | 0 | 0.715 | 0.715 | 0.715 | 0.715 |  |
| add-fk-fkchecks-off | inplace | 1 | 1 | 0 | 0.434 | 0.434 | 0.434 | 0.434 |  |
| add-fk-fkchecks-off | nocopy | 1 | 1 | 0 | 0.499 | 0.499 | 0.499 | 0.499 |  |
| add-fk-fkchecks-off | instant | 1 | 0 | 1 |  |  |  |  | (1846, 'ALGORITHM=INSTANT is not supported. Reason: ADD INDEX. Try ALGORITHM=NOCOPY') |


## Workload latency per phase (ms)

`low_sample=True` means fewer than 30 statements in that phase: percentiles are not meaningful (typically the ALTER was too short to overlap many workload statements; use a larger dataset).

| change | algorithm | alter_status | operation | phase | count | low_sample | success | errors | avg_ms | p50_ms | p95_ms | p99_ms | max_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| change-type | default | success | DELETE | after | 76 | False | 76 | 0 | 0.98 | 0.89 | 2.30 | 3.03 | 3.08 |
| change-type | default | success | DELETE | baseline | 64 | False | 64 | 0 | 1.27 | 0.82 | 5.59 | 7.54 | 7.61 |
| change-type | default | success | INSERT | after | 74 | False | 74 | 0 | 1.85 | 1.58 | 2.89 | 9.45 | 10.66 |
| change-type | default | success | INSERT | baseline | 164 | False | 164 | 0 | 1.58 | 1.46 | 2.46 | 4.48 | 5.92 |
| change-type | default | success | INSERT | during | 2 | True | 2 | 0 | 818.39 | 818.39 | 820.56 | 820.75 | 820.80 |
| change-type | default | success | UPDATE | after | 76 | False | 76 | 0 | 1.01 | 0.99 | 2.02 | 2.67 | 3.71 |
| change-type | default | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.94 | 0.79 | 1.87 | 4.78 | 6.99 |
| change-type | blocking | success | DELETE | after | 76 | False | 76 | 0 | 0.84 | 0.77 | 1.33 | 2.62 | 4.28 |
| change-type | blocking | success | DELETE | baseline | 64 | False | 64 | 0 | 1.21 | 0.78 | 3.91 | 7.68 | 8.73 |
| change-type | blocking | success | INSERT | after | 74 | False | 74 | 0 | 1.41 | 1.33 | 1.84 | 3.28 | 3.67 |
| change-type | blocking | success | INSERT | baseline | 164 | False | 164 | 0 | 1.67 | 1.42 | 2.89 | 7.30 | 9.20 |
| change-type | blocking | success | INSERT | during | 2 | True | 2 | 0 | 861.31 | 861.31 | 862.48 | 862.59 | 862.61 |
| change-type | blocking | success | UPDATE | after | 76 | False | 76 | 0 | 0.84 | 0.80 | 1.44 | 1.71 | 2.00 |
| change-type | blocking | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.93 | 0.79 | 1.70 | 4.75 | 7.19 |
| change-type | copy | failure | DELETE | after | 76 | False | 76 | 0 | 0.92 | 0.79 | 1.40 | 3.31 | 7.68 |
| change-type | copy | failure | DELETE | baseline | 68 | False | 68 | 0 | 1.91 | 0.91 | 7.84 | 11.57 | 12.17 |
| change-type | copy | failure | INSERT | after | 76 | False | 76 | 0 | 1.44 | 1.44 | 1.86 | 2.03 | 2.04 |
| change-type | copy | failure | INSERT | baseline | 168 | False | 168 | 0 | 2.02 | 1.46 | 6.30 | 12.32 | 13.30 |
| change-type | copy | failure | UPDATE | after | 76 | False | 76 | 0 | 0.99 | 0.82 | 1.83 | 3.53 | 7.61 |
| change-type | copy | failure | UPDATE | baseline | 168 | False | 168 | 0 | 1.44 | 0.84 | 6.37 | 17.19 | 21.82 |
| change-type | copy-shared | success | DELETE | after | 76 | False | 76 | 0 | 0.86 | 0.78 | 1.40 | 2.35 | 2.51 |
| change-type | copy-shared | success | DELETE | baseline | 62 | False | 62 | 0 | 1.37 | 0.93 | 3.98 | 7.27 | 7.92 |
| change-type | copy-shared | success | INSERT | after | 74 | False | 74 | 0 | 1.51 | 1.40 | 2.32 | 3.69 | 4.36 |
| change-type | copy-shared | success | INSERT | baseline | 162 | False | 162 | 0 | 1.62 | 1.38 | 2.39 | 6.70 | 11.51 |
| change-type | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 819.94 | 819.94 | 828.17 | 828.90 | 829.09 |
| change-type | copy-shared | success | UPDATE | after | 76 | False | 76 | 0 | 0.90 | 0.90 | 1.60 | 2.75 | 3.40 |
| change-type | copy-shared | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.94 | 0.80 | 1.79 | 3.90 | 11.35 |
| change-type | inplace | failure | DELETE | after | 70 | False | 70 | 0 | 1.05 | 0.68 | 2.27 | 7.62 | 10.90 |
| change-type | inplace | failure | DELETE | baseline | 64 | False | 64 | 0 | 1.12 | 0.93 | 1.73 | 4.84 | 6.54 |
| change-type | inplace | failure | INSERT | after | 70 | False | 70 | 0 | 8.64 | 1.39 | 12.95 | 229.92 | 234.99 |
| change-type | inplace | failure | INSERT | baseline | 164 | False | 164 | 0 | 1.63 | 1.50 | 2.13 | 5.17 | 5.53 |
| change-type | inplace | failure | UPDATE | after | 70 | False | 70 | 0 | 0.87 | 0.66 | 1.99 | 4.50 | 5.79 |
| change-type | inplace | failure | UPDATE | baseline | 164 | False | 164 | 0 | 0.91 | 0.83 | 1.71 | 2.77 | 8.49 |
| change-type | nocopy | failure | DELETE | after | 76 | False | 76 | 0 | 0.96 | 0.74 | 1.67 | 7.47 | 7.63 |
| change-type | nocopy | failure | DELETE | baseline | 64 | False | 64 | 0 | 1.41 | 0.91 | 7.05 | 7.76 | 8.00 |
| change-type | nocopy | failure | INSERT | after | 76 | False | 76 | 0 | 1.75 | 1.36 | 4.64 | 7.71 | 8.41 |
| change-type | nocopy | failure | INSERT | baseline | 164 | False | 164 | 0 | 1.68 | 1.40 | 2.36 | 7.84 | 9.42 |
| change-type | nocopy | failure | UPDATE | after | 76 | False | 76 | 0 | 0.96 | 0.82 | 1.94 | 5.17 | 7.94 |
| change-type | nocopy | failure | UPDATE | baseline | 164 | False | 164 | 0 | 0.94 | 0.73 | 1.77 | 3.33 | 12.00 |
| change-type | instant | failure | DELETE | after | 77 | False | 77 | 0 | 0.64 | 0.57 | 0.91 | 2.02 | 2.74 |
| change-type | instant | failure | DELETE | baseline | 65 | False | 65 | 0 | 1.12 | 0.74 | 3.64 | 5.95 | 8.85 |
| change-type | instant | failure | DELETE | during | 1 | True | 1 | 0 | 4.81 | 4.81 | 4.81 | 4.81 | 4.81 |
| change-type | instant | failure | INSERT | after | 77 | False | 77 | 0 | 1.30 | 1.25 | 1.55 | 2.59 | 4.97 |
| change-type | instant | failure | INSERT | baseline | 165 | False | 165 | 0 | 1.45 | 1.37 | 2.13 | 2.70 | 4.26 |
| change-type | instant | failure | INSERT | during | 1 | True | 1 | 0 | 1.94 | 1.94 | 1.94 | 1.94 | 1.94 |
| change-type | instant | failure | UPDATE | after | 77 | False | 77 | 0 | 0.65 | 0.56 | 0.97 | 2.64 | 7.72 |
| change-type | instant | failure | UPDATE | baseline | 165 | False | 165 | 0 | 0.79 | 0.73 | 1.62 | 2.07 | 3.97 |
| change-type | instant | failure | UPDATE | during | 1 | True | 1 | 0 | 5.30 | 5.30 | 5.30 | 5.30 | 5.30 |
| add-index | default | success | DELETE | after | 76 | False | 76 | 0 | 0.82 | 0.74 | 1.39 | 1.98 | 2.14 |
| add-index | default | success | DELETE | baseline | 66 | False | 66 | 0 | 1.19 | 0.85 | 3.75 | 6.20 | 6.63 |
| add-index | default | success | DELETE | during | 8 | True | 8 | 0 | 3.25 | 1.94 | 7.90 | 7.91 | 7.91 |
| add-index | default | success | INSERT | after | 74 | False | 74 | 0 | 1.43 | 1.33 | 2.51 | 3.07 | 3.17 |
| add-index | default | success | INSERT | baseline | 166 | False | 166 | 0 | 1.66 | 1.41 | 4.13 | 5.43 | 7.58 |
| add-index | default | success | INSERT | during | 10 | True | 10 | 0 | 7.48 | 8.54 | 15.45 | 16.00 | 16.14 |
| add-index | default | success | UPDATE | after | 76 | False | 76 | 0 | 0.81 | 0.80 | 1.58 | 1.83 | 2.27 |
| add-index | default | success | UPDATE | baseline | 166 | False | 166 | 0 | 0.92 | 0.80 | 1.73 | 4.17 | 4.97 |
| add-index | default | success | UPDATE | during | 8 | True | 8 | 0 | 2.85 | 1.19 | 7.78 | 7.78 | 7.79 |
| add-index | blocking | success | DELETE | after | 76 | False | 76 | 0 | 0.89 | 0.80 | 1.45 | 2.33 | 3.49 |
| add-index | blocking | success | DELETE | baseline | 62 | False | 62 | 0 | 0.92 | 0.68 | 2.31 | 4.29 | 4.64 |
| add-index | blocking | success | INSERT | after | 74 | False | 74 | 0 | 1.75 | 1.47 | 3.91 | 4.95 | 6.25 |
| add-index | blocking | success | INSERT | baseline | 162 | False | 162 | 0 | 1.53 | 1.35 | 3.25 | 4.88 | 5.54 |
| add-index | blocking | success | INSERT | during | 2 | True | 2 | 0 | 955.30 | 955.30 | 957.09 | 957.25 | 957.29 |
| add-index | blocking | success | UPDATE | after | 76 | False | 76 | 0 | 1.01 | 0.90 | 2.08 | 3.57 | 3.91 |
| add-index | blocking | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.79 | 0.74 | 1.35 | 3.00 | 3.85 |
| add-index | copy | failure | DELETE | after | 77 | False | 77 | 0 | 0.90 | 0.76 | 1.47 | 2.07 | 2.17 |
| add-index | copy | failure | DELETE | baseline | 64 | False | 64 | 0 | 1.50 | 0.76 | 6.61 | 7.76 | 7.80 |
| add-index | copy | failure | DELETE | during | 1 | True | 1 | 0 | 4.85 | 4.85 | 4.85 | 4.85 | 4.85 |
| add-index | copy | failure | INSERT | after | 76 | False | 76 | 0 | 1.52 | 1.43 | 2.17 | 3.13 | 3.52 |
| add-index | copy | failure | INSERT | baseline | 164 | False | 164 | 0 | 1.55 | 1.32 | 2.97 | 5.39 | 8.78 |
| add-index | copy | failure | INSERT | during | 2 | True | 2 | 0 | 6.17 | 6.17 | 6.38 | 6.40 | 6.41 |
| add-index | copy | failure | UPDATE | after | 76 | False | 76 | 0 | 0.96 | 0.89 | 1.86 | 2.63 | 3.59 |
| add-index | copy | failure | UPDATE | baseline | 164 | False | 164 | 0 | 0.88 | 0.74 | 1.78 | 3.60 | 4.65 |
| add-index | copy | failure | UPDATE | during | 2 | True | 2 | 0 | 2.33 | 2.33 | 4.03 | 4.18 | 4.22 |
| add-index | copy-shared | success | DELETE | after | 78 | False | 78 | 0 | 0.75 | 0.64 | 1.16 | 2.39 | 6.12 |
| add-index | copy-shared | success | DELETE | baseline | 62 | False | 62 | 0 | 1.05 | 0.86 | 3.21 | 3.70 | 3.72 |
| add-index | copy-shared | success | INSERT | after | 76 | False | 76 | 0 | 1.32 | 1.26 | 1.77 | 4.57 | 6.92 |
| add-index | copy-shared | success | INSERT | baseline | 162 | False | 162 | 0 | 1.60 | 1.41 | 3.07 | 6.15 | 7.00 |
| add-index | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 916.37 | 916.37 | 920.12 | 920.46 | 920.54 |
| add-index | copy-shared | success | UPDATE | after | 78 | False | 78 | 0 | 0.80 | 0.70 | 1.51 | 2.77 | 4.84 |
| add-index | copy-shared | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.91 | 0.81 | 1.87 | 3.62 | 4.68 |
| add-index | inplace | success | DELETE | after | 76 | False | 76 | 0 | 0.99 | 0.76 | 1.63 | 4.18 | 8.42 |
| add-index | inplace | success | DELETE | baseline | 62 | False | 62 | 0 | 1.22 | 0.89 | 3.87 | 5.53 | 7.68 |
| add-index | inplace | success | DELETE | during | 8 | True | 8 | 0 | 3.21 | 2.06 | 7.93 | 7.93 | 7.93 |
| add-index | inplace | success | INSERT | after | 74 | False | 74 | 0 | 1.54 | 1.41 | 2.30 | 4.13 | 6.11 |
| add-index | inplace | success | INSERT | baseline | 162 | False | 162 | 0 | 1.56 | 1.43 | 2.40 | 4.18 | 6.67 |
| add-index | inplace | success | INSERT | during | 10 | True | 10 | 0 | 10.58 | 8.53 | 22.75 | 24.87 | 25.40 |
| add-index | inplace | success | UPDATE | after | 75 | False | 75 | 0 | 0.84 | 0.77 | 1.46 | 2.86 | 3.19 |
| add-index | inplace | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.97 | 0.85 | 1.84 | 4.03 | 5.41 |
| add-index | inplace | success | UPDATE | during | 9 | True | 9 | 0 | 4.38 | 2.44 | 12.06 | 14.42 | 15.01 |
| add-index | nocopy | success | DELETE | after | 74 | False | 74 | 0 | 0.87 | 0.72 | 1.68 | 2.56 | 3.79 |
| add-index | nocopy | success | DELETE | baseline | 60 | False | 60 | 0 | 1.12 | 0.79 | 3.71 | 5.87 | 7.22 |
| add-index | nocopy | success | DELETE | during | 8 | True | 8 | 0 | 3.39 | 1.93 | 7.94 | 8.00 | 8.01 |
| add-index | nocopy | success | INSERT | after | 74 | False | 74 | 0 | 2.26 | 1.32 | 3.45 | 31.05 | 31.40 |
| add-index | nocopy | success | INSERT | baseline | 160 | False | 160 | 0 | 1.75 | 1.44 | 3.86 | 7.07 | 8.77 |
| add-index | nocopy | success | INSERT | during | 8 | True | 8 | 0 | 9.14 | 7.63 | 20.39 | 22.26 | 22.73 |
| add-index | nocopy | success | UPDATE | after | 74 | False | 74 | 0 | 0.79 | 0.75 | 1.39 | 2.05 | 2.77 |
| add-index | nocopy | success | UPDATE | baseline | 160 | False | 160 | 0 | 1.00 | 0.82 | 2.62 | 3.66 | 5.10 |
| add-index | nocopy | success | UPDATE | during | 8 | True | 8 | 0 | 2.81 | 1.31 | 7.95 | 7.96 | 7.96 |
| add-index | instant | failure | DELETE | after | 76 | False | 76 | 0 | 0.82 | 0.77 | 1.22 | 1.99 | 2.52 |
| add-index | instant | failure | DELETE | baseline | 62 | False | 62 | 0 | 1.21 | 0.68 | 5.40 | 8.11 | 9.12 |
| add-index | instant | failure | INSERT | after | 76 | False | 76 | 0 | 1.43 | 1.36 | 2.15 | 2.65 | 3.32 |
| add-index | instant | failure | INSERT | baseline | 162 | False | 162 | 0 | 1.42 | 1.26 | 2.77 | 4.99 | 5.68 |
| add-index | instant | failure | UPDATE | after | 76 | False | 76 | 0 | 0.86 | 0.81 | 1.45 | 2.42 | 4.26 |
| add-index | instant | failure | UPDATE | baseline | 162 | False | 162 | 0 | 0.85 | 0.71 | 1.57 | 4.30 | 7.64 |
| widen-column-60 | default | success | DELETE | after | 78 | False | 78 | 0 | 0.74 | 0.65 | 1.18 | 2.23 | 3.96 |
| widen-column-60 | default | success | DELETE | baseline | 64 | False | 64 | 0 | 1.32 | 0.83 | 3.58 | 7.48 | 8.15 |
| widen-column-60 | default | success | INSERT | after | 77 | False | 77 | 0 | 1.58 | 1.29 | 2.59 | 6.84 | 9.49 |
| widen-column-60 | default | success | INSERT | baseline | 164 | False | 164 | 0 | 1.57 | 1.37 | 2.50 | 6.31 | 7.84 |
| widen-column-60 | default | success | INSERT | during | 1 | True | 1 | 0 | 2.39 | 2.39 | 2.39 | 2.39 | 2.39 |
| widen-column-60 | default | success | UPDATE | after | 78 | False | 78 | 0 | 0.81 | 0.70 | 1.82 | 3.11 | 3.92 |
| widen-column-60 | default | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.93 | 0.75 | 1.59 | 4.15 | 9.12 |
| widen-column-60 | blocking | success | DELETE | after | 76 | False | 76 | 0 | 0.90 | 0.76 | 2.00 | 2.55 | 3.09 |
| widen-column-60 | blocking | success | DELETE | baseline | 68 | False | 68 | 0 | 1.26 | 0.84 | 4.07 | 6.97 | 7.50 |
| widen-column-60 | blocking | success | INSERT | after | 74 | False | 74 | 0 | 1.81 | 1.28 | 2.31 | 16.14 | 20.84 |
| widen-column-60 | blocking | success | INSERT | baseline | 168 | False | 168 | 0 | 1.54 | 1.44 | 2.11 | 4.54 | 6.01 |
| widen-column-60 | blocking | success | INSERT | during | 2 | True | 2 | 0 | 728.36 | 728.36 | 730.19 | 730.35 | 730.39 |
| widen-column-60 | blocking | success | UPDATE | after | 76 | False | 76 | 0 | 0.93 | 0.80 | 1.76 | 4.45 | 7.84 |
| widen-column-60 | blocking | success | UPDATE | baseline | 168 | False | 168 | 0 | 0.90 | 0.79 | 1.63 | 4.94 | 7.73 |
| widen-column-60 | copy | failure | DELETE | after | 78 | False | 78 | 0 | 0.96 | 0.79 | 1.98 | 5.18 | 5.48 |
| widen-column-60 | copy | failure | DELETE | baseline | 62 | False | 62 | 0 | 1.17 | 0.74 | 3.92 | 7.69 | 7.78 |
| widen-column-60 | copy | failure | INSERT | after | 78 | False | 78 | 0 | 1.52 | 1.37 | 2.84 | 4.59 | 8.43 |
| widen-column-60 | copy | failure | INSERT | baseline | 162 | False | 162 | 0 | 1.56 | 1.35 | 3.10 | 5.01 | 5.86 |
| widen-column-60 | copy | failure | UPDATE | after | 78 | False | 78 | 0 | 0.96 | 0.88 | 1.91 | 4.80 | 5.11 |
| widen-column-60 | copy | failure | UPDATE | baseline | 162 | False | 162 | 0 | 0.91 | 0.72 | 2.04 | 4.92 | 8.75 |
| widen-column-60 | copy-shared | success | DELETE | after | 75 | False | 75 | 0 | 0.93 | 0.90 | 1.32 | 2.07 | 3.61 |
| widen-column-60 | copy-shared | success | DELETE | baseline | 66 | False | 66 | 0 | 1.08 | 0.73 | 3.90 | 6.27 | 6.41 |
| widen-column-60 | copy-shared | success | DELETE | during | 1 | True | 1 | 0 | 0.43 | 0.43 | 0.43 | 0.43 | 0.43 |
| widen-column-60 | copy-shared | success | INSERT | after | 74 | False | 74 | 0 | 1.62 | 1.57 | 2.26 | 4.03 | 4.68 |
| widen-column-60 | copy-shared | success | INSERT | baseline | 166 | False | 166 | 0 | 1.50 | 1.31 | 2.24 | 6.25 | 8.80 |
| widen-column-60 | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 701.24 | 701.24 | 707.20 | 707.73 | 707.86 |
| widen-column-60 | copy-shared | success | UPDATE | after | 75 | False | 75 | 0 | 1.06 | 0.82 | 1.86 | 6.60 | 8.34 |
| widen-column-60 | copy-shared | success | UPDATE | baseline | 166 | False | 166 | 0 | 0.88 | 0.73 | 1.92 | 4.00 | 5.02 |
| widen-column-60 | copy-shared | success | UPDATE | during | 1 | True | 1 | 0 | 0.60 | 0.60 | 0.60 | 0.60 | 0.60 |
| widen-column-60 | inplace | success | DELETE | after | 76 | False | 76 | 0 | 0.61 | 0.62 | 0.80 | 0.90 | 0.98 |
| widen-column-60 | inplace | success | DELETE | baseline | 64 | False | 64 | 0 | 1.33 | 0.74 | 3.61 | 9.30 | 10.18 |
| widen-column-60 | inplace | success | DELETE | during | 2 | True | 2 | 0 | 19.26 | 19.26 | 31.86 | 32.98 | 33.26 |
| widen-column-60 | inplace | success | INSERT | after | 76 | False | 76 | 0 | 1.31 | 1.31 | 1.58 | 1.81 | 2.00 |
| widen-column-60 | inplace | success | INSERT | baseline | 164 | False | 164 | 0 | 1.66 | 1.48 | 2.95 | 6.12 | 7.37 |
| widen-column-60 | inplace | success | INSERT | during | 2 | True | 2 | 0 | 4.98 | 4.98 | 5.40 | 5.44 | 5.45 |
| widen-column-60 | inplace | success | UPDATE | after | 76 | False | 76 | 0 | 0.64 | 0.60 | 0.90 | 1.98 | 4.98 |
| widen-column-60 | inplace | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.99 | 0.81 | 1.99 | 4.80 | 5.87 |
| widen-column-60 | inplace | success | UPDATE | during | 2 | True | 2 | 0 | 3.17 | 3.17 | 3.17 | 3.17 | 3.17 |
| widen-column-60 | nocopy | success | DELETE | after | 76 | False | 76 | 0 | 0.90 | 0.79 | 1.37 | 3.65 | 3.87 |
| widen-column-60 | nocopy | success | DELETE | baseline | 62 | False | 62 | 0 | 1.22 | 0.99 | 3.56 | 4.30 | 4.82 |
| widen-column-60 | nocopy | success | INSERT | after | 74 | False | 74 | 0 | 1.40 | 1.35 | 1.97 | 2.40 | 3.11 |
| widen-column-60 | nocopy | success | INSERT | baseline | 162 | False | 162 | 0 | 1.56 | 1.42 | 2.46 | 4.69 | 8.07 |
| widen-column-60 | nocopy | success | INSERT | during | 2 | True | 2 | 0 | 10.85 | 10.85 | 11.64 | 11.71 | 11.72 |
| widen-column-60 | nocopy | success | UPDATE | after | 76 | False | 76 | 0 | 0.86 | 0.84 | 1.48 | 1.85 | 2.29 |
| widen-column-60 | nocopy | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.91 | 0.78 | 1.92 | 4.20 | 5.17 |
| widen-column-60 | instant | success | DELETE | after | 78 | False | 78 | 0 | 0.80 | 0.76 | 1.30 | 1.59 | 1.65 |
| widen-column-60 | instant | success | DELETE | baseline | 62 | False | 62 | 0 | 0.94 | 0.75 | 1.54 | 5.00 | 5.74 |
| widen-column-60 | instant | success | INSERT | after | 76 | False | 76 | 0 | 1.36 | 1.34 | 1.91 | 2.31 | 2.88 |
| widen-column-60 | instant | success | INSERT | baseline | 162 | False | 162 | 0 | 1.74 | 1.45 | 2.87 | 6.99 | 9.26 |
| widen-column-60 | instant | success | INSERT | during | 2 | True | 2 | 0 | 29.77 | 29.77 | 29.83 | 29.84 | 29.84 |
| widen-column-60 | instant | success | UPDATE | after | 78 | False | 78 | 0 | 0.82 | 0.79 | 1.45 | 2.12 | 2.62 |
| widen-column-60 | instant | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.87 | 0.75 | 1.71 | 3.45 | 3.98 |
| widen-column-100 | default | success | DELETE | after | 78 | False | 78 | 0 | 1.03 | 0.75 | 1.47 | 10.45 | 11.70 |
| widen-column-100 | default | success | DELETE | baseline | 64 | False | 64 | 0 | 1.45 | 0.80 | 7.09 | 8.23 | 8.27 |
| widen-column-100 | default | success | INSERT | after | 76 | False | 76 | 0 | 1.44 | 1.41 | 1.85 | 2.78 | 5.23 |
| widen-column-100 | default | success | INSERT | baseline | 164 | False | 164 | 0 | 1.72 | 1.51 | 2.74 | 6.29 | 8.29 |
| widen-column-100 | default | success | INSERT | during | 2 | True | 2 | 0 | 20.30 | 20.30 | 20.94 | 21.00 | 21.01 |
| widen-column-100 | default | success | UPDATE | after | 78 | False | 78 | 0 | 0.94 | 0.85 | 1.65 | 3.32 | 6.81 |
| widen-column-100 | default | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.93 | 0.80 | 1.82 | 3.93 | 4.60 |
| widen-column-100 | blocking | success | DELETE | after | 76 | False | 76 | 0 | 0.83 | 0.74 | 1.46 | 1.84 | 2.01 |
| widen-column-100 | blocking | success | DELETE | baseline | 64 | False | 64 | 0 | 1.18 | 0.88 | 3.57 | 5.07 | 5.09 |
| widen-column-100 | blocking | success | INSERT | after | 74 | False | 74 | 0 | 1.45 | 1.43 | 1.82 | 2.10 | 2.32 |
| widen-column-100 | blocking | success | INSERT | baseline | 164 | False | 164 | 0 | 1.87 | 1.42 | 4.10 | 10.07 | 17.21 |
| widen-column-100 | blocking | success | INSERT | during | 2 | True | 2 | 0 | 722.47 | 722.47 | 722.85 | 722.88 | 722.89 |
| widen-column-100 | blocking | success | UPDATE | after | 76 | False | 76 | 0 | 0.84 | 0.85 | 1.37 | 1.74 | 2.03 |
| widen-column-100 | blocking | success | UPDATE | baseline | 164 | False | 164 | 0 | 1.01 | 0.82 | 2.34 | 6.74 | 7.45 |
| widen-column-100 | copy | failure | DELETE | after | 78 | False | 78 | 0 | 0.95 | 0.69 | 1.61 | 7.15 | 7.91 |
| widen-column-100 | copy | failure | DELETE | baseline | 66 | False | 66 | 0 | 1.36 | 0.75 | 5.69 | 8.76 | 11.10 |
| widen-column-100 | copy | failure | INSERT | after | 78 | False | 78 | 0 | 1.35 | 1.27 | 2.12 | 3.77 | 5.11 |
| widen-column-100 | copy | failure | INSERT | baseline | 166 | False | 166 | 0 | 1.49 | 1.38 | 2.12 | 3.99 | 5.23 |
| widen-column-100 | copy | failure | UPDATE | after | 78 | False | 78 | 0 | 0.77 | 0.72 | 1.59 | 2.76 | 4.14 |
| widen-column-100 | copy | failure | UPDATE | baseline | 166 | False | 166 | 0 | 0.84 | 0.76 | 1.58 | 3.34 | 4.62 |
| widen-column-100 | copy-shared | success | DELETE | after | 74 | False | 74 | 0 | 0.80 | 0.79 | 1.28 | 1.43 | 1.45 |
| widen-column-100 | copy-shared | success | DELETE | baseline | 62 | False | 62 | 0 | 1.41 | 0.93 | 6.25 | 7.85 | 7.97 |
| widen-column-100 | copy-shared | success | DELETE | during | 2 | True | 2 | 0 | 0.88 | 0.88 | 0.98 | 0.99 | 0.99 |
| widen-column-100 | copy-shared | success | INSERT | after | 74 | False | 74 | 0 | 1.62 | 1.46 | 2.62 | 4.75 | 4.79 |
| widen-column-100 | copy-shared | success | INSERT | baseline | 162 | False | 162 | 0 | 1.63 | 1.45 | 2.18 | 5.39 | 5.77 |
| widen-column-100 | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 927.99 | 927.99 | 932.42 | 932.82 | 932.91 |
| widen-column-100 | copy-shared | success | UPDATE | after | 74 | False | 74 | 0 | 0.92 | 0.93 | 1.60 | 2.00 | 2.08 |
| widen-column-100 | copy-shared | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.86 | 0.82 | 1.64 | 2.47 | 3.92 |
| widen-column-100 | copy-shared | success | UPDATE | during | 2 | True | 2 | 0 | 0.83 | 0.83 | 1.35 | 1.40 | 1.41 |
| widen-column-100 | inplace | success | DELETE | after | 76 | False | 76 | 0 | 0.84 | 0.76 | 1.20 | 1.88 | 3.53 |
| widen-column-100 | inplace | success | DELETE | baseline | 64 | False | 64 | 0 | 0.97 | 0.73 | 2.71 | 3.52 | 3.72 |
| widen-column-100 | inplace | success | INSERT | after | 74 | False | 74 | 0 | 1.52 | 1.50 | 1.90 | 2.36 | 2.56 |
| widen-column-100 | inplace | success | INSERT | baseline | 164 | False | 164 | 0 | 1.65 | 1.44 | 2.56 | 5.94 | 8.13 |
| widen-column-100 | inplace | success | INSERT | during | 2 | True | 2 | 0 | 5.40 | 5.40 | 8.61 | 8.90 | 8.97 |
| widen-column-100 | inplace | success | UPDATE | after | 76 | False | 76 | 0 | 0.94 | 0.94 | 1.68 | 2.42 | 3.58 |
| widen-column-100 | inplace | success | UPDATE | baseline | 164 | False | 164 | 0 | 1.05 | 0.77 | 2.63 | 6.70 | 9.23 |
| widen-column-100 | nocopy | success | DELETE | after | 77 | False | 77 | 0 | 0.65 | 0.57 | 0.88 | 2.00 | 4.06 |
| widen-column-100 | nocopy | success | DELETE | baseline | 62 | False | 62 | 0 | 1.11 | 0.80 | 3.60 | 5.88 | 6.77 |
| widen-column-100 | nocopy | success | DELETE | during | 1 | True | 1 | 0 | 29.59 | 29.59 | 29.59 | 29.59 | 29.59 |
| widen-column-100 | nocopy | success | INSERT | after | 76 | False | 76 | 0 | 1.46 | 1.31 | 2.21 | 4.44 | 5.34 |
| widen-column-100 | nocopy | success | INSERT | baseline | 162 | False | 162 | 0 | 1.78 | 1.38 | 3.44 | 12.29 | 18.44 |
| widen-column-100 | nocopy | success | INSERT | during | 2 | True | 2 | 0 | 12.54 | 12.54 | 22.21 | 23.07 | 23.28 |
| widen-column-100 | nocopy | success | UPDATE | after | 77 | False | 77 | 0 | 0.64 | 0.64 | 1.24 | 1.91 | 2.03 |
| widen-column-100 | nocopy | success | UPDATE | baseline | 162 | False | 162 | 0 | 0.81 | 0.75 | 1.66 | 3.24 | 4.67 |
| widen-column-100 | nocopy | success | UPDATE | during | 1 | True | 1 | 0 | 4.12 | 4.12 | 4.12 | 4.12 | 4.12 |
| widen-column-100 | instant | success | DELETE | after | 77 | False | 77 | 0 | 0.58 | 0.52 | 0.77 | 1.68 | 3.92 |
| widen-column-100 | instant | success | DELETE | baseline | 59 | False | 59 | 0 | 1.21 | 0.83 | 4.01 | 6.28 | 7.22 |
| widen-column-100 | instant | success | DELETE | during | 1 | True | 1 | 0 | 35.98 | 35.98 | 35.98 | 35.98 | 35.98 |
| widen-column-100 | instant | success | INSERT | after | 77 | False | 77 | 0 | 1.22 | 1.22 | 1.46 | 1.64 | 1.66 |
| widen-column-100 | instant | success | INSERT | baseline | 159 | False | 159 | 0 | 2.18 | 1.48 | 4.68 | 18.59 | 25.77 |
| widen-column-100 | instant | success | INSERT | during | 1 | True | 1 | 0 | 4.64 | 4.64 | 4.64 | 4.64 | 4.64 |
| widen-column-100 | instant | success | UPDATE | after | 77 | False | 77 | 0 | 0.57 | 0.53 | 0.95 | 1.86 | 4.04 |
| widen-column-100 | instant | success | UPDATE | baseline | 159 | False | 159 | 0 | 0.93 | 0.85 | 1.60 | 4.01 | 7.57 |
| widen-column-100 | instant | success | UPDATE | during | 1 | True | 1 | 0 | 1.33 | 1.33 | 1.33 | 1.33 | 1.33 |
| add-fk | default | success | DELETE | after | 76 | False | 76 | 0 | 1.07 | 0.73 | 2.71 | 6.17 | 8.64 |
| add-fk | default | success | DELETE | baseline | 58 | False | 58 | 0 | 1.26 | 0.84 | 3.90 | 7.90 | 8.04 |
| add-fk | default | success | INSERT | after | 74 | False | 74 | 0 | 1.38 | 1.31 | 2.09 | 3.24 | 3.32 |
| add-fk | default | success | INSERT | baseline | 158 | False | 158 | 0 | 1.54 | 1.41 | 3.16 | 4.62 | 5.14 |
| add-fk | default | success | INSERT | during | 2 | True | 2 | 0 | 4.54 | 4.54 | 7.23 | 7.47 | 7.53 |
| add-fk | default | success | UPDATE | after | 74 | False | 74 | 0 | 0.87 | 0.88 | 1.50 | 1.87 | 1.88 |
| add-fk | default | success | UPDATE | baseline | 158 | False | 158 | 0 | 0.86 | 0.74 | 1.62 | 5.40 | 7.95 |
| add-fk | default | success | UPDATE | during | 2 | True | 2 | 0 | 1913.87 | 1913.87 | 1915.12 | 1915.23 | 1915.26 |
| add-fk | blocking | success | DELETE | after | 76 | False | 76 | 0 | 0.97 | 0.80 | 1.67 | 5.97 | 6.16 |
| add-fk | blocking | success | DELETE | baseline | 61 | False | 61 | 0 | 1.11 | 0.72 | 3.73 | 5.56 | 7.58 |
| add-fk | blocking | success | INSERT | after | 74 | False | 74 | 0 | 1.49 | 1.43 | 1.98 | 2.35 | 2.62 |
| add-fk | blocking | success | INSERT | baseline | 161 | False | 161 | 0 | 1.44 | 1.35 | 2.15 | 3.55 | 4.65 |
| add-fk | blocking | success | INSERT | during | 2 | True | 2 | 0 | 835.99 | 835.99 | 1586.08 | 1652.75 | 1669.42 |
| add-fk | blocking | success | UPDATE | after | 75 | False | 75 | 0 | 1.15 | 0.93 | 2.06 | 6.18 | 15.15 |
| add-fk | blocking | success | UPDATE | baseline | 161 | False | 161 | 0 | 0.82 | 0.71 | 1.47 | 3.98 | 4.08 |
| add-fk | blocking | success | UPDATE | during | 1 | True | 1 | 0 | 1729.98 | 1729.98 | 1729.98 | 1729.98 | 1729.98 |
| add-fk | copy | failure | DELETE | after | 78 | False | 78 | 0 | 0.78 | 0.65 | 1.40 | 3.65 | 4.06 |
| add-fk | copy | failure | DELETE | baseline | 62 | False | 62 | 0 | 1.17 | 0.83 | 3.49 | 7.06 | 8.00 |
| add-fk | copy | failure | INSERT | after | 77 | False | 77 | 0 | 1.34 | 1.20 | 2.88 | 3.78 | 4.80 |
| add-fk | copy | failure | INSERT | baseline | 162 | False | 162 | 0 | 1.69 | 1.38 | 2.09 | 10.18 | 17.02 |
| add-fk | copy | failure | INSERT | during | 1 | True | 1 | 0 | 4.29 | 4.29 | 4.29 | 4.29 | 4.29 |
| add-fk | copy | failure | UPDATE | after | 78 | False | 78 | 0 | 1.03 | 0.78 | 2.51 | 6.09 | 7.80 |
| add-fk | copy | failure | UPDATE | baseline | 162 | False | 162 | 0 | 0.79 | 0.74 | 1.50 | 2.78 | 4.17 |
| add-fk | copy-shared | success | DELETE | after | 76 | False | 76 | 0 | 0.94 | 0.91 | 1.34 | 1.98 | 2.03 |
| add-fk | copy-shared | success | DELETE | baseline | 64 | False | 64 | 0 | 1.11 | 0.87 | 3.14 | 4.11 | 5.10 |
| add-fk | copy-shared | success | INSERT | after | 74 | False | 74 | 0 | 1.58 | 1.53 | 2.09 | 2.78 | 3.03 |
| add-fk | copy-shared | success | INSERT | baseline | 164 | False | 164 | 0 | 1.80 | 1.47 | 3.31 | 9.36 | 12.67 |
| add-fk | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 1880.37 | 1880.37 | 1884.12 | 1884.46 | 1884.54 |
| add-fk | copy-shared | success | UPDATE | after | 76 | False | 76 | 0 | 1.01 | 1.07 | 1.64 | 1.89 | 2.04 |
| add-fk | copy-shared | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.92 | 0.85 | 1.74 | 3.27 | 6.00 |
| add-fk | inplace | failure | DELETE | after | 80 | False | 80 | 0 | 0.63 | 0.49 | 1.00 | 3.89 | 3.92 |
| add-fk | inplace | failure | DELETE | baseline | 66 | False | 66 | 0 | 1.32 | 0.92 | 2.70 | 8.97 | 10.53 |
| add-fk | inplace | failure | INSERT | after | 80 | False | 80 | 0 | 1.39 | 1.16 | 2.05 | 4.86 | 5.12 |
| add-fk | inplace | failure | INSERT | baseline | 166 | False | 166 | 0 | 1.78 | 1.41 | 5.07 | 7.95 | 7.99 |
| add-fk | inplace | failure | UPDATE | after | 80 | False | 80 | 0 | 0.77 | 0.55 | 1.07 | 7.40 | 7.92 |
| add-fk | inplace | failure | UPDATE | baseline | 166 | False | 166 | 0 | 0.82 | 0.72 | 1.65 | 2.40 | 4.26 |
| add-fk | nocopy | failure | DELETE | after | 78 | False | 78 | 0 | 0.62 | 0.56 | 0.94 | 1.72 | 3.97 |
| add-fk | nocopy | failure | DELETE | baseline | 65 | False | 65 | 0 | 1.10 | 0.82 | 3.57 | 5.32 | 7.30 |
| add-fk | nocopy | failure | DELETE | during | 1 | True | 1 | 0 | 3.90 | 3.90 | 3.90 | 3.90 | 3.90 |
| add-fk | nocopy | failure | INSERT | after | 78 | False | 78 | 0 | 1.40 | 1.27 | 1.74 | 5.08 | 5.08 |
| add-fk | nocopy | failure | INSERT | baseline | 165 | False | 165 | 0 | 1.61 | 1.39 | 3.64 | 5.14 | 7.08 |
| add-fk | nocopy | failure | INSERT | during | 1 | True | 1 | 0 | 4.84 | 4.84 | 4.84 | 4.84 | 4.84 |
| add-fk | nocopy | failure | UPDATE | after | 78 | False | 78 | 0 | 0.76 | 0.61 | 0.96 | 4.13 | 11.21 |
| add-fk | nocopy | failure | UPDATE | baseline | 165 | False | 165 | 0 | 0.89 | 0.72 | 2.22 | 4.56 | 4.75 |
| add-fk | nocopy | failure | UPDATE | during | 1 | True | 1 | 0 | 0.44 | 0.44 | 0.44 | 0.44 | 0.44 |
| add-fk | instant | failure | DELETE | after | 76 | False | 76 | 0 | 0.87 | 0.74 | 1.34 | 2.77 | 3.21 |
| add-fk | instant | failure | DELETE | baseline | 63 | False | 63 | 0 | 0.98 | 0.84 | 1.64 | 4.30 | 4.88 |
| add-fk | instant | failure | DELETE | during | 1 | True | 1 | 0 | 3.59 | 3.59 | 3.59 | 3.59 | 3.59 |
| add-fk | instant | failure | INSERT | after | 76 | False | 76 | 0 | 1.52 | 1.34 | 2.11 | 5.12 | 6.32 |
| add-fk | instant | failure | INSERT | baseline | 163 | False | 163 | 0 | 1.64 | 1.38 | 3.28 | 6.86 | 8.62 |
| add-fk | instant | failure | INSERT | during | 1 | True | 1 | 0 | 4.91 | 4.91 | 4.91 | 4.91 | 4.91 |
| add-fk | instant | failure | UPDATE | after | 76 | False | 76 | 0 | 1.06 | 0.94 | 1.66 | 4.14 | 10.55 |
| add-fk | instant | failure | UPDATE | baseline | 163 | False | 163 | 0 | 0.84 | 0.77 | 1.61 | 3.15 | 6.71 |
| add-fk | instant | failure | UPDATE | during | 1 | True | 1 | 0 | 0.62 | 0.62 | 0.62 | 0.62 | 0.62 |
| add-fk-fkchecks-off | default | success | DELETE | after | 76 | False | 76 | 0 | 1.06 | 0.80 | 1.53 | 8.82 | 11.46 |
| add-fk-fkchecks-off | default | success | DELETE | baseline | 65 | False | 65 | 0 | 1.11 | 0.77 | 3.93 | 4.53 | 5.33 |
| add-fk-fkchecks-off | default | success | DELETE | during | 11 | True | 11 | 0 | 2.40 | 0.60 | 6.54 | 7.35 | 7.55 |
| add-fk-fkchecks-off | default | success | INSERT | after | 74 | False | 74 | 0 | 1.63 | 1.49 | 2.41 | 4.32 | 6.03 |
| add-fk-fkchecks-off | default | success | INSERT | baseline | 165 | False | 165 | 0 | 1.63 | 1.36 | 3.75 | 6.99 | 12.18 |
| add-fk-fkchecks-off | default | success | INSERT | during | 13 | True | 13 | 0 | 4.48 | 3.65 | 11.66 | 13.19 | 13.57 |
| add-fk-fkchecks-off | default | success | UPDATE | after | 76 | False | 76 | 0 | 0.95 | 0.89 | 1.78 | 3.28 | 3.53 |
| add-fk-fkchecks-off | default | success | UPDATE | baseline | 165 | False | 165 | 0 | 0.92 | 0.74 | 2.14 | 4.71 | 7.11 |
| add-fk-fkchecks-off | default | success | UPDATE | during | 11 | True | 11 | 0 | 0.77 | 0.43 | 2.08 | 2.15 | 2.17 |
| add-fk-fkchecks-off | blocking | success | DELETE | after | 76 | False | 76 | 0 | 0.75 | 0.72 | 1.01 | 1.69 | 2.55 |
| add-fk-fkchecks-off | blocking | success | DELETE | baseline | 60 | False | 60 | 0 | 1.24 | 0.85 | 3.94 | 6.99 | 7.60 |
| add-fk-fkchecks-off | blocking | success | INSERT | after | 74 | False | 74 | 0 | 1.58 | 1.54 | 2.20 | 2.68 | 3.50 |
| add-fk-fkchecks-off | blocking | success | INSERT | baseline | 160 | False | 160 | 0 | 1.51 | 1.44 | 2.19 | 3.03 | 3.86 |
| add-fk-fkchecks-off | blocking | success | INSERT | during | 2 | True | 2 | 0 | 779.85 | 779.85 | 781.32 | 781.45 | 781.49 |
| add-fk-fkchecks-off | blocking | success | UPDATE | after | 76 | False | 76 | 0 | 0.80 | 0.81 | 1.24 | 1.58 | 2.07 |
| add-fk-fkchecks-off | blocking | success | UPDATE | baseline | 160 | False | 160 | 0 | 0.87 | 0.77 | 1.62 | 4.80 | 7.55 |
| add-fk-fkchecks-off | copy | failure | DELETE | after | 76 | False | 76 | 0 | 0.79 | 0.69 | 1.33 | 2.57 | 3.84 |
| add-fk-fkchecks-off | copy | failure | DELETE | baseline | 60 | False | 60 | 0 | 1.02 | 0.71 | 3.63 | 6.49 | 7.31 |
| add-fk-fkchecks-off | copy | failure | INSERT | after | 76 | False | 76 | 0 | 1.36 | 1.34 | 1.93 | 2.04 | 2.13 |
| add-fk-fkchecks-off | copy | failure | INSERT | baseline | 160 | False | 160 | 0 | 1.54 | 1.24 | 3.54 | 6.96 | 7.35 |
| add-fk-fkchecks-off | copy | failure | UPDATE | after | 76 | False | 76 | 0 | 0.85 | 0.81 | 1.59 | 1.78 | 1.78 |
| add-fk-fkchecks-off | copy | failure | UPDATE | baseline | 160 | False | 160 | 0 | 0.76 | 0.57 | 1.68 | 5.92 | 9.62 |
| add-fk-fkchecks-off | copy-shared | success | DELETE | after | 74 | False | 74 | 0 | 0.85 | 0.76 | 1.46 | 1.88 | 1.91 |
| add-fk-fkchecks-off | copy-shared | success | DELETE | baseline | 64 | False | 64 | 0 | 1.12 | 0.87 | 2.87 | 6.42 | 6.91 |
| add-fk-fkchecks-off | copy-shared | success | INSERT | after | 72 | False | 72 | 0 | 1.55 | 1.54 | 2.08 | 2.47 | 2.49 |
| add-fk-fkchecks-off | copy-shared | success | INSERT | baseline | 164 | False | 164 | 0 | 1.51 | 1.38 | 2.03 | 5.15 | 5.49 |
| add-fk-fkchecks-off | copy-shared | success | INSERT | during | 2 | True | 2 | 0 | 734.32 | 734.32 | 739.39 | 739.84 | 739.95 |
| add-fk-fkchecks-off | copy-shared | success | UPDATE | after | 74 | False | 74 | 0 | 0.92 | 0.87 | 1.79 | 2.90 | 3.75 |
| add-fk-fkchecks-off | copy-shared | success | UPDATE | baseline | 164 | False | 164 | 0 | 0.77 | 0.73 | 1.47 | 2.53 | 3.75 |
| add-fk-fkchecks-off | inplace | success | DELETE | after | 76 | False | 76 | 0 | 0.98 | 0.71 | 1.73 | 7.67 | 7.72 |
| add-fk-fkchecks-off | inplace | success | DELETE | baseline | 60 | False | 60 | 0 | 1.28 | 0.77 | 3.80 | 7.37 | 7.87 |
| add-fk-fkchecks-off | inplace | success | DELETE | during | 14 | True | 14 | 0 | 1.35 | 1.28 | 2.82 | 2.94 | 2.97 |
| add-fk-fkchecks-off | inplace | success | INSERT | after | 76 | False | 76 | 0 | 1.73 | 1.54 | 3.11 | 6.88 | 9.01 |
| add-fk-fkchecks-off | inplace | success | INSERT | baseline | 160 | False | 160 | 0 | 1.51 | 1.38 | 2.29 | 4.05 | 5.17 |
| add-fk-fkchecks-off | inplace | success | INSERT | during | 14 | True | 14 | 0 | 4.58 | 3.98 | 9.85 | 11.65 | 12.10 |
| add-fk-fkchecks-off | inplace | success | UPDATE | after | 76 | False | 76 | 0 | 1.10 | 0.87 | 3.43 | 6.30 | 6.61 |
| add-fk-fkchecks-off | inplace | success | UPDATE | baseline | 160 | False | 160 | 0 | 0.84 | 0.78 | 1.49 | 4.62 | 6.15 |
| add-fk-fkchecks-off | inplace | success | UPDATE | during | 14 | True | 14 | 0 | 0.83 | 0.57 | 2.17 | 2.30 | 2.33 |
| add-fk-fkchecks-off | nocopy | success | DELETE | after | 72 | False | 72 | 0 | 1.19 | 0.88 | 1.98 | 9.75 | 11.94 |
| add-fk-fkchecks-off | nocopy | success | DELETE | baseline | 65 | False | 65 | 0 | 0.89 | 0.70 | 1.95 | 4.18 | 5.76 |
| add-fk-fkchecks-off | nocopy | success | DELETE | during | 17 | True | 17 | 0 | 1.39 | 0.96 | 2.96 | 6.06 | 6.84 |
| add-fk-fkchecks-off | nocopy | success | INSERT | after | 72 | False | 72 | 0 | 2.85 | 1.65 | 9.91 | 13.26 | 15.91 |
| add-fk-fkchecks-off | nocopy | success | INSERT | baseline | 165 | False | 165 | 0 | 1.58 | 1.38 | 2.30 | 6.35 | 8.06 |
| add-fk-fkchecks-off | nocopy | success | INSERT | during | 17 | True | 17 | 0 | 4.75 | 2.79 | 12.45 | 13.83 | 14.18 |
| add-fk-fkchecks-off | nocopy | success | UPDATE | after | 72 | False | 72 | 0 | 1.31 | 0.94 | 3.09 | 10.17 | 13.49 |
| add-fk-fkchecks-off | nocopy | success | UPDATE | baseline | 165 | False | 165 | 0 | 0.77 | 0.70 | 1.57 | 2.05 | 2.90 |
| add-fk-fkchecks-off | nocopy | success | UPDATE | during | 17 | True | 17 | 0 | 1.56 | 1.03 | 3.98 | 4.07 | 4.09 |
| add-fk-fkchecks-off | instant | failure | DELETE | after | 77 | False | 77 | 0 | 0.84 | 0.75 | 1.27 | 1.73 | 2.87 |
| add-fk-fkchecks-off | instant | failure | DELETE | baseline | 60 | False | 60 | 0 | 1.08 | 0.80 | 2.35 | 5.18 | 5.70 |
| add-fk-fkchecks-off | instant | failure | DELETE | during | 1 | True | 1 | 0 | 0.89 | 0.89 | 0.89 | 0.89 | 0.89 |
| add-fk-fkchecks-off | instant | failure | INSERT | after | 76 | False | 76 | 0 | 1.49 | 1.34 | 2.31 | 3.93 | 4.77 |
| add-fk-fkchecks-off | instant | failure | INSERT | baseline | 160 | False | 160 | 0 | 1.70 | 1.38 | 2.18 | 10.72 | 13.62 |
| add-fk-fkchecks-off | instant | failure | INSERT | during | 2 | True | 2 | 0 | 4.58 | 4.58 | 6.76 | 6.95 | 7.00 |
| add-fk-fkchecks-off | instant | failure | UPDATE | after | 76 | False | 76 | 0 | 1.00 | 1.03 | 1.74 | 2.57 | 3.28 |
| add-fk-fkchecks-off | instant | failure | UPDATE | baseline | 160 | False | 160 | 0 | 0.85 | 0.73 | 1.87 | 2.71 | 3.17 |
| add-fk-fkchecks-off | instant | failure | UPDATE | during | 2 | True | 2 | 0 | 4.70 | 4.70 | 5.33 | 5.39 | 5.40 |


## Figures

- fig_alter_duration.png
- fig_workload_p95.png
- fig_latency_distribution.png
- fig_workload_errors.png: not generated (no applicable data)
