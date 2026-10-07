-- Expected to be refused with error 1846 when foreign_key_checks is ON (verify on your server).
ALTER TABLE orders ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id),
  ALGORITHM=INPLACE, LOCK=NONE;
