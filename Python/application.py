# SELECT (with JOIN) / Aggregation Logic

def get_total_quantity_per_supplier_python(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT s.id, s.supplier_name, p.quantity_in_stock FROM Supplier s JOIN Product p ON s.id = p.supplier_id")
        rows = cursor.fetchall()

        # Create a dictionary to store total quantities per supplier
        supplier_totals = {}
        for row in rows:
            supplier_id, supplier_name, quantity = row
            if supplier_id not in supplier_totals:
                supplier_totals[supplier_id] = {"supplier_name": supplier_name, "total_quantity": 0}
            supplier_totals[supplier_id]["total_quantity"] += quantity

        # Convert the dictionary values to a list of tuples
        result = [(data["supplier_name"], data["total_quantity"]) for data in supplier_totals.values()]
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")
        raise
    finally:
        cursor.close()

# GROUP BY / filter
        
def filter_grouped_data(group):
    # Assuming you want to keep rows where 'B' is equal to the maximum value of 'B' within each group
    max_b_value = group['B'].max()
    return group[group['B'] == max_b_value]