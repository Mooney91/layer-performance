DELIMITER //

CREATE PROCEDURE GetProductsWithTotalValue()
BEGIN
    DECLARE total_value DECIMAL(65, 30) DEFAULT 0;

    -- Create a temporary table to store product data
    CREATE TEMPORARY TABLE temp_products
    SELECT
        id,
        product_name,
        quantity_in_stock,
        unit_price,
        (quantity_in_stock * unit_price) AS product_value
    FROM Product;

    -- Calculate the total value of all products
    SELECT SUM(product_value) INTO total_value FROM temp_products;

    -- Retrieve product data along with total value
    SELECT
        id,
        product_name,
        quantity_in_stock,
        unit_price,
        product_value,
        total_value AS total_product_value
    FROM temp_products;

    -- Clean up: drop the temporary table
    DROP TEMPORARY TABLE IF EXISTS temp_products;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE RecordTransaction(
    IN productID INT,
    IN transactionType ENUM('Inbound', 'Outbound'),
    IN transactionQuantity INT,
    IN employeeID INT,
    OUT transactionID INT
)
BEGIN
    DECLARE currentQuantity INT;
    DECLARE errorMessage VARCHAR(255);
    
    -- Check if product exists and has sufficient quantity for outbound transaction
    IF transactionType = 'Outbound' THEN
        SELECT quantity_in_stock INTO currentQuantity FROM Product WHERE id = productID;
        IF currentQuantity IS NULL THEN
            SET errorMessage = CONCAT('Product with ID ', productID, ' does not exist.');
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = errorMessage;
        END IF;
        
        IF currentQuantity < transactionQuantity THEN
            SET errorMessage = CONCAT('Insufficient quantity for product with ID ', productID);
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = errorMessage;
        END IF;
    END IF;

    -- Update product quantity in stock
    IF transactionType = 'Inbound' THEN
        UPDATE Product SET quantity_in_stock = quantity_in_stock + transactionQuantity WHERE id = productID;
    ELSE
        UPDATE Product SET quantity_in_stock = quantity_in_stock - transactionQuantity WHERE id = productID;
    END IF;

    -- Record transaction
    INSERT INTO `Transaction` (product_id, transaction_type, quantity, transaction_date, employee_id) 
    VALUES (productID, transactionType, transactionQuantity, CURDATE(), employeeID);
    
    -- Get the ID of the newly inserted transaction record
    SELECT LAST_INSERT_ID() INTO transactionID;
END //

DELIMITER ;
