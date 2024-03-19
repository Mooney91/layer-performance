def select_all_employees(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Employee")
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"The error '{e}' occurred")
        raise
    finally:
        cursor.close()

# SELECT (with JOIN) / Aggregation Logic

def get_total_quantity_per_supplier(connection):
    try:
        cursor = connection.cursor()
        query = """
            SELECT s.supplier_name, SUM(p.quantity_in_stock) AS total_quantity
            FROM Supplier s
            JOIN Product p ON s.id = p.supplier_id
            GROUP BY s.supplier_name
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"The error '{e}' occurred")
        raise
    finally:
        cursor.close()

# GROUP BY / filter

def select_filtered_employees(connection):
    try:
        cursor = connection.cursor()
        # Modify the SQL query to include the desired filter
        query = """
            SELECT *
            FROM Employee
            WHERE department = 'Shipping and Receiving'  -- Example filter: Keep only employees in the Sales department
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"The error '{e}' occurred")
        raise
    finally:
        cursor.close()

# ORDER BY / sort

def select_and_sort_employees(connection, sort_column="employee_name"):
    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM Employee ORDER BY {sort_column}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"The error '{e}' occurred")
        raise
    finally:
        cursor.close()

