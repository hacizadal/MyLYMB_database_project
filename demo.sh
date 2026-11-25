#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python configure.py
python -m pip install -r requirements.txt
docker compose up -d --wait
bash sweep.sh --rows 1000 --repeats 2 --changes "widen-column-60 widen-column-rebuild change-type" --algorithms "instant copy blocking" --baseline-secs 2 --after-secs 2
