"""Preserve individual measurements and environment metadata."""
import sys, platform, os, json
from pathlib import Path
import pandas as pd
from common import connect
p=Path(sys.argv[1]); df=pd.read_csv(p/'alter_results.csv'); 
from outcomes import classify_outcome
df['outcome'] = df.apply(lambda r: classify_outcome(r['change'], r['requested_algorithm'], r['status'], r.get('errno')), axis=1)
df.to_csv(p/'individual_runs.csv', index=False)
ok=df[df.status=='success']
ok.groupby(['change','requested_algorithm']).duration_seconds.agg(['count','mean','median','std','min','max']).to_csv(p/'repeated_statistics.csv')
if (df.outcome == 'unexpected_failure').any():
    print('WARNING: unexpected failures; inspect individual_runs.csv')
with connect() as c:
    with c.cursor() as cur:
        cur.execute('SELECT VERSION(), @@innodb_buffer_pool_size, @@character_set_server'); server=cur.fetchone()
(p/'environment.json').write_text(json.dumps(dict(platform=platform.platform(), processor=platform.processor(), logical_cpus=os.cpu_count(), server=server),indent=2))
print('Individual measurements:',p/'alter_results.csv')
