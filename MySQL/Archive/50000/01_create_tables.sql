DROP TABLE IF EXISTS `Transaction`;
DROP TABLE IF EXISTS `Employee`;
DROP TABLE IF EXISTS `Product`;
DROP TABLE IF EXISTS `Supplier`;

CREATE TABLE IF NOT EXISTS `Supplier` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS `Product` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    quantity_in_stock INT,
    unit_price DECIMAL(10, 2),
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES Supplier(id)
);

CREATE TABLE IF NOT EXISTS `Employee` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(255) NOT NULL,
    department VARCHAR(100),
    job_title VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS `Transaction` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    transaction_type ENUM('Inbound', 'Outbound') NOT NULL,
    quantity INT,
    transaction_date DATE,
    employee_id INT,
    FOREIGN KEY (product_id) REFERENCES Product(id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id)
);
