#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python configure.py
docker compose up -d --wait
id="final_$(date -u +%Y%m%d_%H%M%S)"
bash sweep.sh --rows "${ROWS:-100000}" --repeats "${REPEATS:-5}" --threads "${THREADS:-4}" --interval 0.01 --sweep-id "$id"
python advanced_experiments.py --out "results/$id/advanced.csv"
python research_summary.py "results/$id"
