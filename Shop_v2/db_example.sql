use first_db;
CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(30),
    available_quantity FLOAT,
    price_per_kg FLOAT
    );
CREATE TABLE admin (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(30),
    password VARCHAR(50)
    );
CREATE TABLE clients (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(30) NOT NULL,
    password VARCHAR(50) NOT NULL
    );

-- 
-- update products
-- -- set product_name = "Rosii";
-- -- SELECT * from products;
-- -- update products
-- -- set product_name = "Castraveti";

-- -- select * from products;

INSERT INTO products(name, available_quantity, price_per_kg) VALUES 
('Rosii', 36.0, 3.0),
('Castraveti', 2.0, 2.5),
('Ardei', 4.0, 4.0),
('Ceapa', 0.0, 2.0);
SELECT * from products;

INSERT INTO admin(user_name, password) VALUES
('admin', 1234), ('admin2', 5678);
INSERT INTO clients(user_name, password) VALUES
('user', 1234), ('user2', 4567);

SELECT * FROM admin;
SELECT * FROM clients;


