LOAD DATA INFILE '/var/lib/mysql-files/supplier_data.csv' INTO TABLE Supplier FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' (supplier_name, contact_person, phone_number, email);
LOAD DATA INFILE '/var/lib/mysql-files/product_data.csv' INTO TABLE Product FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' (product_name, category, quantity_in_stock, unit_price, supplier_id);
LOAD DATA INFILE '/var/lib/mysql-files/employee_data.csv' INTO TABLE Employee FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' (employee_name, department, job_title);
LOAD DATA INFILE '/var/lib/mysql-files/transaction_data.csv' INTO TABLE Transaction FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n' (product_id, transaction_type, quantity, transaction_date, employee_id);
