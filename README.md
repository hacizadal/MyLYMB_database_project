# MyLYMB_database_project

## Leyla: setup and reset fixes

Run these commands in PowerShell inside the project folder:

```powershell
python -m pip install pymysql mysql-connector-python Faker
docker compose up -d
docker compose ps
```

Wait until `mariadb-lab` is healthy. Then run one test:

```powershell
python run_alter.py --change add-index --algorithm inplace
```

Each call now automatically:
1. Drops `orders` first, then `user_table` (deletes their lab data).
2. Loads `schema.sql` using the correct password argument `-plabpass`.
3. Generates 1,000,000 users and commits each batch.
4. Executes `SELECT COUNT(*) FROM user_table` and requires exactly 1,000,000.
5. Runs and times the ALTER, then appends its result to `results_alter.csv`.

The reset/generation time is excluded from the ALTER duration. Generation may
 take several minutes. A reset, insert, or count failure stops the test before
 the ALTER. Earlier committed batches can remain after a generation failure;
 the next reset removes them.

To reset and verify the baseline without running an ALTER:

```powershell
python reset_database.py
```

To compare the two existing index algorithms:

```powershell
python run_alter.py --change add-index --algorithm inplace
python run_alter.py --change add-index --algorithm nocopy
```

Both commands reset automatically. Do not manually drop the index between them.
Old CSV results are retained; they were produced before these baseline fixes.

## Team integration

Yasmine should add the `orders` CREATE TABLE statement after `user_table` in
`schema.sql`; its reset DROP statement is already present. This change does not
implement the other teammates' tasks.

For concurrent tests, finish reset and count verification **before** starting
`workload.py`. The team's orchestrator should call `reset_database()` once,
then start the workload and ALTER without a second reset. Do not start the
workload before the current `run_alter.py` call: it resets the tables first.

Current dependencies include both database drivers because existing scripts
use different drivers. The shared dependency/driver cleanup belongs to Mirqe.
