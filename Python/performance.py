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
        employees = select_all_employees(connection)
        filtered_employees = employees.groupby('A').apply(filter_grouped_data)
        connection.close()
        return render_template('index.html', employees=filtered_employees)
    else:
        return "Failed to establish connection to the database."
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
