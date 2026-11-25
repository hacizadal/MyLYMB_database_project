#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export REPL_LAB_PASSWORD="$(python -c 'import secrets; print(secrets.token_hex(24))')"
project="mylymb-repl-$(python -c 'import secrets; print(secrets.token_hex(4))')"
compose=(docker compose -p "$project" -f docker-compose.replication.yml)
cleanup() { "${compose[@]}" down -v; }
trap cleanup EXIT
"${compose[@]}" up -d --wait
python replication_benchmark.py --rows "${ROWS:-100000}" --repeats "${REPEATS:-3}"
