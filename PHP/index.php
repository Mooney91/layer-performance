<?php

// Database configuration
$databaseHost = 'data-mysql';
$databaseUsername = 'user';
$databasePassword = 'password';
$databaseName = 'MySQL';
$databasePort = 3306;

// Connect to MySQL
$conn = new mysqli($databaseHost, $databaseUsername, $databasePassword, $databaseName, $databasePort);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Function to select all employees
function selectAllEmployees($conn) {
    $query = "SELECT * FROM Employee";
    $result = $conn->query($query);
    $employees = [];
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $employees[] = $row;
        }
    }
    return $employees;
}

// SELECT (with JOIN) / Aggregation Logic
function getTotalQuantityPerSupplier($conn) {
    $query = "
        SELECT s.supplier_name, SUM(p.quantity_in_stock) AS total_quantity
        FROM Supplier s
        JOIN Product p ON s.id = p.supplier_id
        GROUP BY s.supplier_name";
    $result = $conn->query($query);
    $supplierQuantities = [];
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $supplierQuantities[] = $row;
        }
    }
    return $supplierQuantities;
}

// // Route 'handling
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Set the content type
    header('Content-Type: application/json');

    // Route handling
    switch ($_SERVER['REQUEST_URI']) {
        case '/select-mysql':
            $employees = selectAllEmployees($conn);
            // echo json_encode($employees);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;
        case '/aggregation-mysql':
            $supplierQuantities = getTotalQuantityPerSupplier($conn);
            // echo json_encode($supplierQuantities);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;
            
            break;
        case '/aggregation-php':
            // Function to perform aggregation in PHP
            function getTotalQuantityPerSupplierPHP($conn) {
                $supplierQuery = "SELECT * FROM Supplier";
                $supplierResult = $conn->query($supplierQuery);
        
                if ($supplierResult === false) {
                    // Handle error
                    echo json_encode(array("message" => "Failed to execute query"));
                    return;
                }
        
                $productQuery = "SELECT * FROM Product";
                $productResult = $conn->query($productQuery);
        
                if ($productResult === false) {
                    // Handle error
                    echo json_encode(array("message" => "Failed to execute query"));
                    return;
                }
        
                $aggregatedData = array();
        
                while ($productRow = $productResult->fetch_assoc()) {
                    $supplierId = $productRow['supplier_id'];
                    $quantityInStock = $productRow['quantity_in_stock'];
        
                    $supplierResult->data_seek(0); // Reset pointer to start
                    while ($supplierRow = $supplierResult->fetch_assoc()) {
                        if ($supplierRow['id'] === $supplierId) {
                            $supplierName = $supplierRow['supplier_name'];
                            if (array_key_exists($supplierName, $aggregatedData)) {
                                $aggregatedData[$supplierName] += $quantityInStock;
                            } else {
                                $aggregatedData[$supplierName] = $quantityInStock;
                            }
                            break; // Break the inner loop once matched
                        }
                    }
                }
        
                $result = array();
                foreach ($aggregatedData as $supplierName => $totalQuantity) {
                    $result[] = array(
                        'supplier_name' => $supplierName,
                        'total_quantity' => $totalQuantity
                    );
                }
        
                return $result;
            }
        
            // Call the function to perform aggregation in PHP
            $supplierQuantitiesPHP = getTotalQuantityPerSupplierPHP($conn);
            // echo json_encode($supplierQuantitiesPHP);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;
        
        case '/filter-mysql':
            function filterEmployees($conn) {
                $query = "SELECT * FROM Employee WHERE department = 'Shipping and Receiving'";
                $result = $conn->query($query);
                $filteredEmployees = [];
                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        $filteredEmployees[] = $row;
                    }
                }
                return $filteredEmployees;
            }
        
            // Call the function to filter employees
            $filteredEmployees = filterEmployees($conn);
            // echo json_encode($filteredEmployees);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;

        case '/filter-php':
            // Function to filter employees in PHP
            function filterEmployeesPHP($conn) {
                $query = "SELECT * FROM Employee";
                $result = $conn->query($query);
        
                if ($result === false) {
                    // Handle error
                    echo json_encode(array("message" => "Failed to execute query"));
                    return;
                }
        
                $filteredResults = array();
                while ($row = $result->fetch_assoc()) {
                    if ($row['department'] === 'Shipping and Receiving') {
                        $filteredResults[] = $row;
                    }
                }
        
                return $filteredResults;
            }
        
            // Call the function to filter employees
            $filteredEmployeesPHP = filterEmployeesPHP($conn);
            if (!isset($filteredEmployeesPHP)) {
                break;
            }
        
            // Render template with filtered employees
            // echo json_encode(array("employees" => $filteredEmployeesPHP));

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;
            
            
        case '/sorting-mysql':
            // Function to select and sort employees in MySQL
            function selectAndSortEmployees($conn) {
                $query = "SELECT * FROM Employee ORDER BY employee_name";
                $result = $conn->query($query);
                $sortedEmployees = [];
                if ($result->num_rows > 0) {
                    while ($row = $result->fetch_assoc()) {
                        $sortedEmployees[] = $row;
                    }
                }
                return $sortedEmployees;
            }

            // Call the function to select and sort employees
            $sortedEmployees = selectAndSortEmployees($conn);
            // echo json_encode($sortedEmployees);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;

        case '/sorting-php':
            // Function to sort employees by name
            function sortEmployeesByName($employees) {
                if (!is_array($employees)) {
                    // Handle error
                    echo json_encode(array("message" => "Employees is not an array"));
                    return array();
                }
        
                // Sort employees by name (PHP-based sorting)
                usort($employees, function($a, $b) {
                    return strcmp($a['employee_name'], $b['employee_name']);
                });
        
                return $employees;
            }
        
            // Call the function to select all employees
            $employeesPHP = selectAllEmployees($conn);
            if (!isset($employeesPHP)) {
                break;
            }
        
            // Call the function to sort employees by name
            $sortedEmployeesPHP = sortEmployeesByName($employeesPHP);

            // echo json_encode($sortedEmployeesPHP);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;
            
        case '/procedure-mysql':
            // Function to call stored procedure in MySQL
            function callStoredProcedure($conn) {
                // Assuming 'GetProductsWithTotalValue' is the name of your stored procedure
                $query = "CALL GetProductsWithTotalValue()";
                $result = $conn->query($query);

                // Check if the procedure call was successful
                if ($result === false) {
                    // Handle error
                    echo json_encode(array("message" => "Failed to execute stored procedure"));
                    return;
                }

                // Fetch all rows from the result set
                $products = [];
                while ($row = $result->fetch_assoc()) {
                    $products[] = $row;
                }
                return $products;
            }

            // Call the function to call stored procedure
            $products = callStoredProcedure($conn);

            // echo json_encode($products);

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;

        case '/procedure-php':
            // Function to retrieve products from the database
            function retrieveProducts($conn) {
                $query = "SELECT id, product_name, quantity_in_stock, unit_price FROM Product";
                $result = $conn->query($query);
        
                if ($result === false) {
                    // Handle error
                    echo json_encode(array("message" => "Failed to execute query"));
                    return;
                }
        
                $products = array();
                while ($row = $result->fetch_assoc()) {
                    $products[] = $row;
                }
        
                return $products;
            }
        
            // Call the function to retrieve products
            $productsPHP = retrieveProducts($conn);
            if (!isset($productsPHP)) {
                break;
            }
        
            // Calculate the total product value
            $totalProductValue = 0;
            foreach ($productsPHP as $product) {
                $totalProductValue += $product['quantity_in_stock'] * $product['unit_price'];
            }
        
            // Render template with products and total product value
            // echo json_encode(array("products" => $productsPHP, "total_product_value" => $totalProductValue));

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;
            
        case '/advanced-procedure-mysql':
            // Function to call advanced stored procedure in MySQL
            function callAdvancedStoredProcedure($conn) {
                // Assuming 'RecordTransaction' is the name of your advanced stored procedure
                $query = "CALL RecordTransaction(4, 'Inbound', 5, 1, @transactionID)";
                $result = $conn->query($query);

                // Check if the procedure call was successful
                if ($result === false) {
                    // Handle error
                    echo json_encode(array("message" => "Failed to execute stored procedure"));
                    return;
                }

                // After the procedure call, execute another query to get the value of @transactionID
                $transactionIDResult = $conn->query("SELECT @transactionID as transactionID");
                $transactionIDRow = $transactionIDResult->fetch_assoc();
                $transactionID = $transactionIDRow['transactionID'];

                // Return transaction ID
                return $transactionID;
            }

            // Call the function to call advanced stored procedure
            $transactionID = callAdvancedStoredProcedure($conn);

            // echo json_encode(array("message" => "Transaction recorded successfully.", "transactionID" => $transactionID));

            // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;

            break;

        case '/advanced-procedure-php':
            // Function to retrieve quantity in stock for a product
            function retrieveQuantityInStock($conn, $productId) {
                $query = "SELECT quantity_in_stock FROM Product WHERE id = ?";
                $stmt = $conn->prepare($query);
                $stmt->bind_param("i", $productId);
                $stmt->execute();
                $result = $stmt->get_result();
        
                if ($result === false || $result->num_rows === 0) {
                    // Handle error or product not found
                    http_response_code(404);
                    echo json_encode(array("message" => "Product does not exist."));
                    return;
                }
        
                $row = $result->fetch_assoc();
                return $row['quantity_in_stock'];
            }
        
            // Function to update quantity in stock for a product and record transaction
            function updateQuantityAndRecordTransaction($conn, $productId, $transactionQuantity) {
                $currentQuantity = retrieveQuantityInStock($conn, $productId);
        
                if (!isset($currentQuantity)) {
                    return;
                }
        
                if ($currentQuantity < $transactionQuantity) {
                    // Insufficient quantity for transaction
                    http_response_code(400);
                    echo json_encode(array("message" => "Insufficient quantity for transaction."));
                    return;
                }
        
                // Start transaction
                $conn->begin_transaction();
        
                // Update quantity in stock
                $queryUpdate = "UPDATE Product SET quantity_in_stock = ? WHERE id = ?";
                $stmtUpdate = $conn->prepare($queryUpdate);
                $newQuantity = $currentQuantity - $transactionQuantity;
                $stmtUpdate->bind_param("ii", $newQuantity, $productId);
                $stmtUpdate->execute();
        
                if ($stmtUpdate === false) {
                    // Rollback transaction and handle error
                    $conn->rollback();
                    http_response_code(500);
                    echo json_encode(array("message" => "Failed to update quantity in stock."));
                    return;
                }
        
                // Record transaction
                $queryInsert = "INSERT INTO Transaction (product_id, transaction_type, quantity, transaction_date, employee_id) VALUES (?, 'Inbound', ?, CURDATE(), 1)";
                $stmtInsert = $conn->prepare($queryInsert);
                $stmtInsert->bind_param("ii", $productId, $transactionQuantity);
                $stmtInsert->execute();
        
                if ($stmtInsert === false) {
                    // Rollback transaction and handle error
                    $conn->rollback();
                    http_response_code(500);
                    echo json_encode(array("message" => "Failed to record transaction."));
                    return;
                }
        
                // Commit transaction
                $conn->commit();
        
                // Transaction recorded successfully
                // echo json_encode(array("message" => "Transaction recorded successfully."));

                // Redirect to index.html if query is successful
                header("Location: index.html");
                exit;
            }
        
            // Call the function to update quantity and record transaction
            updateQuantityAndRecordTransaction($conn, 4, 5);

                        // Redirect to index.html if query is successful
            header("Location: index.html");
            exit;
            break;
        
        default:
            http_response_code(404);
            // echo json_encode(array("message" => "This is Not Found"));
            echo json_encode(array("message" => "This is " . $_SERVER['REQUEST_URI']));
            break;
    };
};

// Close MySQL connection
$conn->close();

