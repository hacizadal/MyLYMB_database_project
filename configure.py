from pathlib import Path
import secrets
p = Path(__file__).resolve().parent / '.env'
if not p.exists():
    p.write_text('MARIADB_ROOT_PASSWORD=' + secrets.token_hex(24) + '\n')
    print('Created local .env')
else:
    print('Keeping existing .env; verify it matches your lab volume')
