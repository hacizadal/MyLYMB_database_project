CREATE TABLE user_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    email_address VARCHAR(30) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    country VARCHAR(30) NOT NULL,
    username VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL
) ENGINE=InnoDB;
