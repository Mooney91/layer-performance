from flask import Flask, render_template
import pandas as pd
from application import *
from data import *

import mysql.connector

app = Flask(__name__)

def create_connection(host_name, user_name, user_password, db_name, port):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port
        )
        print("Connection to MySQL DB successful")
        return connection
    except Exception as e:
        print(f"The error '{e}' occurred")
        raise

# TESTING CONNECTION AND QUERYING
    
@app.route('/select-mysql')
def select_mysql():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        employees = select_all_employees(connection)
        connection.close()
        return render_template('index.html', employees=employees)
    else:
        return "Failed to establish connection to the database."
    
# SELECT (with JOIN) / Aggregation Logic
    
@app.route('/aggregation-mysql')
def aggregation_mysql():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        supplier_quantities = get_total_quantity_per_supplier(connection)
        connection.close()
        return render_template('index.html', supplier_quantities=supplier_quantities)
    else:
        return "Failed to establish connection to the database."

@app.route('/aggregation-python')
def aggregation_python():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        supplier_quantities = get_total_quantity_per_supplier_python(connection)
        connection.close()
        return render_template('index.html', supplier_quantities=supplier_quantities)
    else:
        return "Failed to establish connection to the database."
    
# GROUP BY / filter
    
@app.route('/filter-mysql')
def filter_mysql():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        filtered_employees = select_filtered_employees(connection)
        connection.close()
        return render_template('index.html', employees=filtered_employees)
    else:
        return "Failed to establish connection to the database."
    
@app.route('/filter-python')
def filter_python():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        try:
            cursor = connection.cursor()
            query = """
                SELECT *
                FROM Employee
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
            filtered_df = df[df['department'] == 'Shipping and Receiving']
            connection.close()
            return render_template('index.html', employees=filtered_df.to_html())
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Failed to establish connection to the database."

# ORDER BY / sort

@app.route('/sorting-mysql')
def sorting_mysql():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        # Sort employees by the default column (employee name)
        employees = select_and_sort_employees(connection)
        connection.close()
        return render_template('index.html', employees=employees)
    else:
        return "Failed to establish connection to the database."

@app.route('/sorting-python')
def sorting_python():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        employees = select_all_employees(connection)
        sorted_employees = sort_employees_by_name(employees)
        connection.close()
        return render_template('index.html', employees=sorted_employees)
    else:
        return "Failed to establish connection to the database."

# STORED PROCEDURE

@app.route('/procedure-mysql')
def calling_stored_procedure():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.execute("CALL GetProductsWithTotalValue()")
                # Fetch the result
                result = cursor.fetchall()
                connection.close()
                return render_template('index.html', products=result)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Failed to establish connection to the database."
    
@app.route('/procedure-python')
def retrieve_products_python():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        try:
            with connection.cursor(dictionary=True) as cursor:
                # Retrieve product data
                cursor.execute("SELECT id, product_name, quantity_in_stock, unit_price FROM Product")
                products = cursor.fetchall()

                # Calculate total value of products
                total_product_value = sum(product['quantity_in_stock'] * product['unit_price'] for product in products)

                connection.close()
                return render_template('index.html', products=products, total_product_value=total_product_value)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Failed to establish connection to the database."
    
@app.route('/advanced-procedure-mysql')
def calling_advanced_stored_procedure():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc("RecordTransaction", (4, 'Inbound', 5, 1, "@transactionID"))
                # Fetch the result if any
                connection.commit()  # Commit the transaction
                connection.close()
                 # You can pass additional data to the template if needed
                data = {"message": "Transaction recorded successfully."}
                return render_template('index.html', data=data)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Failed to establish connection to the database."
    
@app.route('/advanced-procedure-python')
def record_transaction():
    custom_port = 3306
    connection = create_connection("data-mysql", "user", "password", "MySQL", custom_port)
    if connection:
        try:
            with connection.cursor() as cursor:
                # Check if product exists and has sufficient quantity
                cursor.execute("SELECT quantity_in_stock FROM Product WHERE id = %s", (4,))
                result = cursor.fetchone()
                if result is None:
                    return "Product does not exist."
                
                current_quantity = result[0]
                transaction_quantity = 5  # Adjust according to your requirement
                
                if current_quantity < transaction_quantity:
                    return "Insufficient quantity for transaction."
                
                # Perform transaction
                cursor.execute("UPDATE Product SET quantity_in_stock = %s WHERE id = %s", (current_quantity - transaction_quantity, 1))
                
                # Record transaction
                cursor.execute("INSERT INTO `Transaction` (product_id, transaction_type, quantity, transaction_date, employee_id) VALUES (%s, %s, %s, CURDATE(), %s)", (1, 'Inbound', transaction_quantity, 1))
                
                connection.commit()
                connection.close()
                # You can pass additional data to the template if needed
                data = {"message": "Transaction recorded successfully."}
                return render_template('index.html', data=data)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    else:
        return "Failed to establish connection to the database."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
