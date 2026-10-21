#!/usr/bin/env python3
"""Check workload statement counts during each ALTER from a completed sweep."""
import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


def parse_time(value):
    return datetime.fromisoformat(value.strip().replace('Z', '+00:00')).astimezone(timezone.utc)


def inspect(sweep_dir, minimum):
    sweep_dir = Path(sweep_dir)
    alter_file = sweep_dir / 'alter_results.csv'
    if not alter_file.is_file():
        raise FileNotFoundError(alter_file)
    results = []
    with alter_file.open(newline='', encoding='utf-8') as f:
        for alter in csv.DictReader(f):
            csv_name = alter.get('workload_csv', '')
            csv_path = Path(csv_name) if csv_name else None
            if csv_path and not csv_path.is_file():
                csv_path = sweep_dir / csv_path.name
            count = errors = 0
            if csv_path and csv_path.is_file():
                start = parse_time(alter['started_at_utc'])
                end = parse_time(alter['ended_at_utc'])
                with csv_path.open(newline='', encoding='utf-8') as wf:
                    for row in csv.DictReader(wf):
                        try:
                            when = parse_time(row['timestamp_utc'])
                        except (KeyError, ValueError):
                            continue
                        if start <= when <= end:
                            count += 1
                            errors += row.get('status') == 'error'
            results.append((alter.get('change', ''), alter.get('requested_algorithm', ''),
                            count, errors, 'OK' if count >= minimum else 'LOW'))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sweep_dir', help='results/sweep_<id>')
    parser.add_argument('--min-statements', type=int, default=1,
                        help='minimum statement starts during each ALTER [1]')
    args = parser.parse_args()
    if args.min_statements < 1:
        parser.error('--min-statements must be >= 1')
    try:
        results = inspect(args.sweep_dir, args.min_statements)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'Cannot check sweep: {exc}\n')
    if not results:
        parser.exit(2, 'No ALTER results found\n')
    print('change,algorithm,during_alter,errors,check')
    for result in results:
        print(','.join(map(str, result)))
    low = sum(row[-1] == 'LOW' for row in results)
    print(f'{len(results)} ALTERs checked; {low} below threshold {args.min_statements}')
    return 1 if low else 0


if __name__ == '__main__':
    raise SystemExit(main())
