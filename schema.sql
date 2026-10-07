-- Drop the child table before its parent so foreign keys do not block reset.
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS user_table;

CREATE TABLE user_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    email_address VARCHAR(100) NOT NULL,
    phone_number VARCHAR(25) NOT NULL,
    country VARCHAR(60) NOT NULL,
    username VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL
) ENGINE=InnoDB;
