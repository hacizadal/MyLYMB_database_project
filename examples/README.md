# Reusable examples
Run only against a fresh disposable lab after `python reset_db.py --rows 1000`. Reset before each statement; these examples change the schema. Use a second connection to observe writes while COPY runs.

```sql
ALTER TABLE user_table MODIFY email_address VARCHAR(60) NOT NULL, ALGORITHM=INSTANT, LOCK=NONE;
ALTER TABLE user_table ADD INDEX idx_username(username), ALGORITHM=NOCOPY, LOCK=NONE;
ALTER TABLE user_table MODIFY birth_date DATETIME NOT NULL, ALGORITHM=COPY, LOCK=NONE;
```

For the blocking baseline repeat the last statement after reset with `LOCK=EXCLUSIVE`. Compare the raw workload CSVs; do not infer availability from DDL duration alone.
