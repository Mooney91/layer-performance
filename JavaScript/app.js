const express = require('express');
const mysql = require('mysql');
const path = require('path');

const app = express();

const connection = mysql.createConnection({
    host: 'data-mysql',
    user: 'user',
    password: 'password',
    database: 'MySQL',
    port: 3306
});

connection.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL database: ', err);
        throw err;
    }
    console.log('Connected to MySQL database');
});

/////////////////////////////////
// Functions
/////////////////////////////////

// Function to select all employees
function selectAllEmployees(callback) {
    connection.query('SELECT * FROM Employee', (err, rows) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            callback(err, null);
            return;
        }
        callback(null, rows);
    });
}

// SELECT (with JOIN) / Aggregation Logic
function getTotalQuantityPerSupplier(callback) {
    connection.query(`
        SELECT s.supplier_name, SUM(p.quantity_in_stock) AS total_quantity
        FROM Supplier s
        JOIN Product p ON s.id = p.supplier_id
        GROUP BY s.supplier_name
    `, (err, rows) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            callback(err, null);
            return;
        }
        callback(null, rows);
    });
}

// GROUP BY / filter
function selectFilteredEmployees(callback) {
    connection.query(`
        SELECT *
        FROM Employee
        WHERE department = 'Shipping and Receiving'
    `, (err, rows) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            callback(err, null);
            return;
        }
        callback(null, rows);
    });
}

// ORDER BY / sort
function selectAndSortEmployees(callback) {
    connection.query(`SELECT * FROM Employee ORDER BY employee_name`, (err, rows) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            callback(err, null);
            return;
        }
        callback(null, rows);
    });
}

// SELECT (with JOIN) / Aggregation Logic
function getTotalQuantityPerSupplierJavascript(callback) {
    connection.query(`
        SELECT * FROM Supplier
    `, (err, supplierRows) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            callback(err, null);
            return;
        }
        
        connection.query(`
            SELECT * FROM Product
        `, (err, productRows) => {
            if (err) {
                console.error('Error executing MySQL query: ', err);
                callback(err, null);
                return;
            }

            const aggregatedData = {};
            productRows.forEach(product => {
                const supplierId = product.supplier_id;
                const quantityInStock = product.quantity_in_stock;

                const supplier = supplierRows.find(supplier => supplier.id === supplierId);
                if (supplier) {
                    const supplierName = supplier.supplier_name;
                    if (aggregatedData[supplierName]) {
                        aggregatedData[supplierName] += quantityInStock;
                    } else {
                        aggregatedData[supplierName] = quantityInStock;
                    }
                }
            });

            const result = Object.entries(aggregatedData).map(([supplierName, totalQuantity]) => ({
                supplier_name: supplierName,
                total_quantity: totalQuantity
            }));

            callback(null, result);
        });
    });
}


// GROUP BY / filter
function filterGroupedData(group) {
    // Assuming you want to keep rows where 'B' is equal to the maximum value of 'B' within each group
    const maxBValue = group.reduce((max, item) => Math.max(max, item.B), -Infinity);
    return group.filter(item => item.B === maxBValue);
}

// ORDER BY / sort
function sortEmployeesByName(employees) {
    if (!Array.isArray(employees)) {
        console.error('Employees is not an array');
        return [];
    }

    // Sort employees by name (JavaScript-based sorting)
    return employees.slice().sort((a, b) => a.employee_name.localeCompare(b.employee_name));
}

/////////////////////////////////
// Routes
/////////////////////////////////

// Route for aggregation in MySQL
app.get('/aggregation-mysql', (req, res) => {
    getTotalQuantityPerSupplier((err, supplierQuantities) => {
        if (err) {
            res.status(500).send('Failed to get total quantity per supplier');
            return;
        }
        res.render('index.html', { supplier_quantities: supplierQuantities });
    });
});

// Route for performing aggregation in Javascript
app.get('/aggregation-javascript', (req, res) => {
    getTotalQuantityPerSupplierJavascript((err, supplierQuantities) => {
        if (err) {
            res.status(500).send('Failed to execute query');
            return;
        }
        res.render('index.html', { supplier_quantities: supplierQuantities });
    });
});

// Route for filtering in MySQL
app.get('/filter-mysql', (req, res) => {
    // Call the function to filter employees
    selectFilteredEmployees((err, filteredEmployees) => {
        if (err) {
            // Handle error
            res.status(500).send('Failed to execute query');
            return;
        }
        // Render template with filtered employees
        res.render('index.html', { employees: filteredEmployees });
    });
});

// Route for filtering in Javascript
app.get('/filter-javascript', (req, res) => {
    connection.query('SELECT * FROM Employee', (err, results) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            res.status(500).send('Failed to execute query');
            return;
        }
        const filteredResults = results.filter(employee => employee.department === 'Shipping and Receiving');
        res.render('index.html', { employees: filteredResults });
    });
});

// Route for sorting in MySQL
app.get('/sorting-mysql', (req, res) => {
    // Call the function to select and sort employees
    selectAndSortEmployees((err, sortedEmployees) => {
        if (err) {
            // Handle error
            res.status(500).send('Failed to execute query');
            return;
        }
        // Render template with sorted employees
        res.render('index.html', { employees: sortedEmployees });
    });
});

// Route for sorting in JavaScript
app.get('/sorting-javascript', (req, res) => {
    // Call the function to select all employees
    selectAllEmployees((err, employees) => {
        if (err) {
            // Handle error
            res.status(500).send('Failed to execute query');
            return;
        }
        // Call the function to sort employees by name
        const sortedEmployees = sortEmployeesByName(employees);
        // Render template with sorted employees
        res.render('index.html', { employees: sortedEmployees });
    });
});

// Route for calling stored procedure in MySQL
app.get('/procedure-mysql', (req, res) => {
    connection.query('CALL GetProductsWithTotalValue()', (err, results) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            res.status(500).send('Failed to execute query');
            return;
        }
        res.render('index.html', { products: results });
    });
});

// Route for retrieving products in Javascript
app.get('/procedure-javascript', (req, res) => {
    connection.query('SELECT id, product_name, quantity_in_stock, unit_price FROM Product', (err, products) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            res.status(500).send('Failed to execute query');
            return;
        }
        const totalProductValue = products.reduce((total, product) => total + (product.quantity_in_stock * product.unit_price), 0);
        res.render('index.html', { products: products, total_product_value: totalProductValue });
    });
});

// Route for calling advanced stored procedure in MySQL
app.get('/advanced-procedure-mysql', (req, res) => {
    connection.query('CALL RecordTransaction(?, ?, ?, ?, @transactionID)', [4, 'Inbound', 5, 1], (err, results) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            res.status(500).send('Failed to execute query');
            return;
        }
        // After the procedure call, execute another query to get the value of @transactionID
        connection.query('SELECT @transactionID as transactionID', (err, rows) => {
            if (err) {
                console.error('Error executing MySQL query: ', err);
                res.status(500).send('Failed to execute query');
                return;
            }
            const transactionID = rows[0].transactionID;
            res.render('index.html', { data: { message: 'Transaction recorded successfully.', transactionID: transactionID } });
        });
    });
});

// Route for recording transaction in Javascript
app.get('/advanced-procedure-javascript', (req, res) => {
    connection.query('SELECT quantity_in_stock FROM Product WHERE id = ?', [4], (err, result) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            res.status(500).send('Failed to execute query');
            return;
        }
        if (!result || !result.length) {
            res.status(404).send('Product does not exist.');
            return;
        }
        const currentQuantity = result[0].quantity_in_stock;
        const transactionQuantity = 5; // Adjust according to your requirement
        if (currentQuantity < transactionQuantity) {
            res.status(400).send('Insufficient quantity for transaction.');
            return;
        }
        connection.query('UPDATE Product SET quantity_in_stock = ? WHERE id = ?', [currentQuantity - transactionQuantity, 1], (err) => {
            if (err) {
                console.error('Error executing MySQL query: ', err);
                res.status(500).send('Failed to execute query');
                return;
            }
            connection.query('INSERT INTO `Transaction` (product_id, transaction_type, quantity, transaction_date, employee_id) VALUES (?, ?, ?, CURDATE(), ?)', [1, 'Inbound', transactionQuantity, 1], (err) => {
                if (err) {
                    console.error('Error executing MySQL query: ', err);
                    res.status(500).send('Failed to execute query');
                    return;
                }
                res.render('index.html', { data: { message: 'Transaction recorded successfully.' } });
            });
        });
    });
});

// Route for selecting all employees
app.get('/select-mysql', (req, res) => {
    selectAllEmployees((err, results) => {
        if (err) {
            console.error('Error executing MySQL query: ', err);
            res.status(500).send('Failed to execute query');
            return;
        }
        res.render('index.html', { employees: results });
    });
});

////////////////////////////////
// Listen and Render
////////////////////////////////

// Set up template engine and static files
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'html');
app.engine('html', require('ejs').renderFile);

// Start server
const PORT = process.env.PORT || 1337;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
