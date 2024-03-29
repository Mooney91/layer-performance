-- DELIMITER //

-- CREATE TRIGGER update_quantity_in_stock AFTER INSERT ON `Transaction`
-- FOR EACH ROW
-- BEGIN
--     DECLARE quantityChange INT;

--     -- Determine the change in quantity based on transaction type
--     IF NEW.transaction_type = 'Inbound' THEN
--         SET quantityChange = NEW.quantity;
--     ELSE
--         SET quantityChange = -NEW.quantity;
--     END IF;

--     -- Update the quantity in stock for the corresponding product
--     UPDATE Product SET quantity_in_stock = quantity_in_stock + quantityChange WHERE id = NEW.product_id;
-- END;
-- //

-- DELIMITER ;