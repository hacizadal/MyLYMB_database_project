-- Table copy, reads allowed, writes wait.
ALTER TABLE orders ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id),
  ALGORITHM=COPY, LOCK=SHARED;
