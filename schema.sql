-- MyLYMB schema. Re-runnable: drops (child first) and recreates both tables.
-- Both tables start WITHOUT secondary indexes and WITHOUT foreign keys on purpose:
-- add-index and add-fk are experiments.

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS user_table;

CREATE TABLE user_table (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    first_name    VARCHAR(50) NOT NULL,
    middle_name   VARCHAR(50),
    last_name     VARCHAR(50) NOT NULL,
    birth_date    DATE NOT NULL,
    email_address VARCHAR(30) NOT NULL,
    phone_number  VARCHAR(25) NOT NULL,
    country       VARCHAR(30) NOT NULL,
    username      VARCHAR(30) NOT NULL,
    created_at    DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Child table for the add-fk experiment. user_id deliberately has no index and no
-- constraint yet; the experiment adds FOREIGN KEY (user_id) REFERENCES user_table(id).
CREATE TABLE orders (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    order_total DECIMAL(10,2) NOT NULL,
    status      VARCHAR(20) NOT NULL,
    created_at  DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
