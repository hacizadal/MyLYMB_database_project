# add-fk: manual SQL scenarios

These files reproduce the four add-fk scenarios by hand in a `mariadb` client. They mirror
what `run_alter.py` executes (`add-fk` and `add-fk-fkchecks-off`) and are meant for
exploration and for checking a result by eye. **The recorded benchmark always goes through
`run_alter.py` / `sweep.sh`** so that timing and CSV format are identical for every experiment.

Reset before each file (each scenario needs an `orders` table without a foreign key):

    python reset_db.py --rows 100000 --change add-fk
    docker exec -i mariadb-lab mariadb -uroot -plabpass schemalab < tests/add-fk/01_default_checks_on.sql

| File | Session setting | ALTER clause |
|---|---|---|
| 01_default_checks_on.sql | foreign_key_checks=1 (default) | none |
| 02_inplace_checks_on.sql | foreign_key_checks=1 | ALGORITHM=INPLACE, LOCK=NONE |
| 03_inplace_checks_off.sql | foreign_key_checks=0 | ALGORITHM=INPLACE, LOCK=NONE |
| 04_copy_checks_on.sql | foreign_key_checks=1 | ALGORITHM=COPY, LOCK=SHARED |

`foreign_key_checks=0` is a **session setting**, not an algorithm. With it OFF, existing rows are
not re-validated against `user_table`: the resulting constraint may cover orphan rows. The
generated dataset contains no orphans, so the comparison stays fair here.
