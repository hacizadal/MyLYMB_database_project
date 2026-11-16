# Patch integration notes (2026-11-16)

- Patch 0001 was already applied to all non-README files in the uploaded repository. The README was merged manually with the pre-existing 100k-row findings retained.
- Patch 0002's independent-check statement is included in README Findings, labeled as separately reported and not independently verified here.
- The additional `results/sandbox_mariadb11.4_1M/` dataset was supplied in patch 0001, labeled MariaDB 11.4.9; it is not a local rerun or the user's 11.4.13 Docker benchmark.
- The focused 8-run `results/sweep_20261116_160234/` from the uploaded ZIP is retained, with raw workload CSVs and analysis. Short ALTERs have low during-window sample counts.
- Original 126-run workload traces remain unavailable; the console-derived results are distinct.
- No Docker database was started or rerun while preparing this ZIP.
