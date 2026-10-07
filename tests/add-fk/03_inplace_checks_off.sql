-- Session setting (NOT an algorithm): skip re-validation of existing rows for this connection only.
SET SESSION foreign_key_checks=0;
ALTER TABLE orders ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id),
  ALGORITHM=INPLACE, LOCK=NONE;
