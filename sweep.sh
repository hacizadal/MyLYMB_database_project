#!/usr/bin/env bash
# Run the whole experiment matrix: every (change x algorithm) on a freshly reset database.
#
# Per run:  reset DB (schema + dataset) -> start workload -> baseline phase -> ALTER
#           -> after phase -> stop workload (SIGTERM) -> results saved -> next run.
#
#   ./sweep.sh --rows 100000
#   ./sweep.sh --rows 1000000 --repeats 3
#   ./sweep.sh --rows 200000 --changes "add-index add-fk-fkchecks-off" --algorithms "inplace nocopy"
#
# Windows: run from Git Bash or WSL (the database itself runs in Docker Desktop).
set -uo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  if command -v python3 >/dev/null 2>&1; then PY=python3; else PY=python; fi
fi

ROWS=100000
CHANGES="change-type add-index widen-column-60 widen-column-100 add-fk add-fk-fkchecks-off"
ALGORITHMS="default blocking copy copy-shared inplace nocopy instant"
BASELINE_SECS=10
AFTER_SECS=5
THREADS=1
INTERVAL=0.05
REPEATS=1
SWEEP_ID="sweep_$(date -u +%Y%m%d_%H%M%S)"
OUT_ROOT="results"
LOCK_TIMEOUT=10

usage() { sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'; cat <<USAGE

Options (defaults in brackets):
  --rows N            rows in user_table (and orders for add-fk) [$ROWS]
  --changes "a b"     experiments to run [all: $CHANGES]
  --algorithms "a b"  algorithms to request [all: $ALGORITHMS]
  --repeats N         repetitions of each combination [$REPEATS]
  --baseline-secs S   workload-only period before the ALTER [$BASELINE_SECS]
  --after-secs S      workload period after the ALTER [$AFTER_SECS]
  --threads N         workload connections [$THREADS]
  --interval S        workload pause between cycles, per thread [$INTERVAL]
  --lock-timeout S    workload lock_wait_timeout [$LOCK_TIMEOUT]
  --sweep-id NAME     output folder name under results/ [$SWEEP_ID]
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
    --rows) ROWS="$2"; shift 2;;
    --changes) CHANGES="$2"; shift 2;;
    --algorithms) ALGORITHMS="$2"; shift 2;;
    --repeats) REPEATS="$2"; shift 2;;
    --baseline-secs) BASELINE_SECS="$2"; shift 2;;
    --after-secs) AFTER_SECS="$2"; shift 2;;
    --threads) THREADS="$2"; shift 2;;
    --interval) INTERVAL="$2"; shift 2;;
    --lock-timeout) LOCK_TIMEOUT="$2"; shift 2;;
    --sweep-id) SWEEP_ID="$2"; shift 2;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 1;;
  esac
done

OUT_DIR="$OUT_ROOT/$SWEEP_ID"
mkdir -p "$OUT_DIR"

"$PY" -c "from common import connect; connect().close()" 2>/dev/null || {
  echo "Cannot connect to MariaDB. Start it with:  docker compose up -d   (then wait until healthy)" >&2
  exit 1
}

WL_PID=""
cleanup() { [ -n "$WL_PID" ] && kill -TERM "$WL_PID" 2>/dev/null && wait "$WL_PID" 2>/dev/null; }
trap cleanup EXIT INT TERM

{
  echo "sweep_id=$SWEEP_ID"; echo "started_utc=$(date -u +%FT%TZ)"; echo "rows=$ROWS"
  echo "changes=$CHANGES"; echo "algorithms=$ALGORITHMS"; echo "repeats=$REPEATS"
  echo "baseline_secs=$BASELINE_SECS"; echo "after_secs=$AFTER_SECS"; echo "threads=$THREADS"
  echo "interval=$INTERVAL"; echo "lock_timeout=$LOCK_TIMEOUT"
  echo "python=$("$PY" --version 2>&1)"
  "$PY" -c "from common import connect; c=connect(); cur=c.cursor(); cur.execute('SELECT VERSION(), @@innodb_buffer_pool_size'); print('server_version=%s\nbuffer_pool_bytes=%s' % cur.fetchone())"
} > "$OUT_DIR/sweep_config.txt"

total=0; for _ in $CHANGES; do for _ in $ALGORITHMS; do total=$((total + REPEATS)); done; done
n=0
echo "Sweep $SWEEP_ID: $total runs, $ROWS rows -> $OUT_DIR"

for change in $CHANGES; do
  case "$change" in add-fk*) PROFILE=orders;; *) PROFILE=user_table;; esac
  for algo in $ALGORITHMS; do
    for rep in $(seq 1 "$REPEATS"); do
      n=$((n + 1))
      tag="${change}_${algo}_r${rep}"
      wl="$OUT_DIR/workload_${tag}.csv"
      ready="$OUT_DIR/.ready_${tag}"; rm -f "$ready"
      echo "[$n/$total] $tag"

      # 1. identical starting state
      "$PY" reset_db.py --rows "$ROWS" --change "$change" >"$OUT_DIR/reset_${tag}.log" 2>&1 \
        || { echo "  reset failed, see $OUT_DIR/reset_${tag}.log" >&2; exit 1; }

      # 2. workload in the background
      "$PY" workload.py --out "$wl" --profile "$PROFILE" --threads "$THREADS" --interval "$INTERVAL" \
        --lock-timeout "$LOCK_TIMEOUT" --ready-file "$ready" 2>"$OUT_DIR/workload_${tag}.log" &
      WL_PID=$!
      for _ in $(seq 1 50); do [ -f "$ready" ] && break; sleep 0.2; done
      [ -f "$ready" ] || { echo "  workload did not start, see $OUT_DIR/workload_${tag}.log" >&2; exit 1; }

      # 3. baseline -> ALTER -> after
      sleep "$BASELINE_SECS"
      "$PY" run_alter.py --change "$change" --algorithm "$algo" --out "$OUT_DIR/alter_results.csv" \
        --tag "$SWEEP_ID" --workload "$OUT_DIR/workload_${tag}.csv" --dataset-rows "$ROWS" \
        --poll-out "$OUT_DIR/processlist_${tag}.csv" | tail -1
      rc=${PIPESTATUS[0]}
      [ "$rc" -ne 0 ] && echo "  run_alter.py infrastructure error (rc=$rc)" >&2
      sleep "$AFTER_SECS"

      # 4. stop workload cleanly
      kill -TERM "$WL_PID" 2>/dev/null; wait "$WL_PID" 2>/dev/null; WL_PID=""
      rm -f "$ready"
    done
  done
done

echo "finished_utc=$(date -u +%FT%TZ)" >> "$OUT_DIR/sweep_config.txt"
echo "Analysing..."
"$PY" analyze_results.py "$OUT_DIR" || echo "analysis failed (raw CSVs are in $OUT_DIR)" >&2
echo "Done. Results: $OUT_DIR"
