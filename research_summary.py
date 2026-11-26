"""Preserve individual measurements and environment metadata."""
import ctypes
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

import pandas as pd

from common import connect
from outcomes import classify_outcome

GIB = 1024 ** 3


def run_text(command):
    """Output of a command as text, or None if it is missing, fails or takes too long."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def total_ram_bytes():
    """Physical RAM of this computer in bytes, or None if it cannot be read."""
    try:
        if sys.platform.startswith('win'):
            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ('length', ctypes.c_ulong),
                    ('memory_load', ctypes.c_ulong),
                    ('total_physical', ctypes.c_ulonglong),
                    ('available_physical', ctypes.c_ulonglong),
                    ('total_page_file', ctypes.c_ulonglong),
                    ('available_page_file', ctypes.c_ulonglong),
                    ('total_virtual', ctypes.c_ulonglong),
                    ('available_virtual', ctypes.c_ulonglong),
                    ('available_extended_virtual', ctypes.c_ulonglong),
                ]
            status = MemoryStatus()
            status.length = ctypes.sizeof(MemoryStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return int(status.total_physical)
        if sys.platform == 'darwin':
            text = run_text(['sysctl', '-n', 'hw.memsize'])
            return int(text) if text else None
        with open('/proc/meminfo', encoding='utf-8') as handle:
            for line in handle:
                if line.startswith('MemTotal:'):
                    return int(line.split()[1]) * 1024
    except (OSError, ValueError, AttributeError):
        return None
    return None


def docker_facts():
    """Docker server version and the memory Docker may use (the limit set in Docker Desktop)."""
    version = run_text(['docker', 'version', '--format', '{{.Server.Version}}'])
    memory = run_text(['docker', 'info', '--format', '{{.MemTotal}}'])
    memory_gib = round(int(memory) / GIB, 1) if memory and memory.isdigit() else None
    return version, memory_gib


def environment(server):
    ram = total_ram_bytes()
    docker_version, docker_memory_gib = docker_facts()
    return dict(
        platform=platform.platform(),
        processor=platform.processor(),
        logical_cpus=os.cpu_count(),
        ram_gib=round(ram / GIB, 1) if ram else None,
        python=platform.python_version(),
        pandas=pd.__version__,
        docker_server_version=docker_version,
        docker_memory_gib=docker_memory_gib,
        server=server,
    )


def main(sweep_dir):
    df = pd.read_csv(sweep_dir / 'alter_results.csv')
    df['outcome'] = df.apply(
        lambda r: classify_outcome(r['change'], r['requested_algorithm'], r['status'], r.get('errno')), axis=1)
    df.to_csv(sweep_dir / 'individual_runs.csv', index=False)
    ok = df[df.status == 'success']
    stats = ok.groupby(['change', 'requested_algorithm']).duration_seconds.agg(
        ['count', 'mean', 'median', 'std', 'min', 'max'])
    stats.to_csv(sweep_dir / 'repeated_statistics.csv')
    if (df.outcome == 'unexpected_failure').any():
        print('WARNING: unexpected failures; inspect individual_runs.csv')
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT VERSION(), @@innodb_buffer_pool_size, @@character_set_server')
            server = cur.fetchone()
    text = json.dumps(environment(server), indent=2)
    (sweep_dir / 'environment.json').write_text(text)
    print('Individual measurements:', sweep_dir / 'alter_results.csv')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
