-- Default: no algorithm clause, foreign_key_checks ON.
ALTER TABLE orders ADD CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES user_table (id);
