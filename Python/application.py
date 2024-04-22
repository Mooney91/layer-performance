# SELECT (with JOIN) / Aggregation Logic

# def get_total_quantity_per_supplier_python(connection):
#     try:
#         cursor = connection.cursor()
#         cursor.execute("SELECT s.id, s.supplier_name, p.quantity_in_stock FROM Supplier s JOIN Product p ON s.id = p.supplier_id")
#         rows = cursor.fetchall()

#         # Create a dictionary to store total quantities per supplier
#         supplier_totals = {}
#         for row in rows:
#             supplier_id, supplier_name, quantity = row
#             if supplier_id not in supplier_totals:
#                 supplier_totals[supplier_id] = {"supplier_name": supplier_name, "total_quantity": 0}
#             supplier_totals[supplier_id]["total_quantity"] += quantity

#         # Convert the dictionary values to a list of tuples
#         result = [(data["supplier_name"], data["total_quantity"]) for data in supplier_totals.values()]
#         return result
#     except Exception as e:
#         print(f"The error '{e}' occurred")
#         raise
#     finally:
#         cursor.close()

# def get_total_quantity_per_supplier_python(connection):
#     try:
#         cursor = connection.cursor()

#         # Fetch Supplier data
#         cursor.execute("SELECT * FROM Supplier")
#         supplier_rows = cursor.fetchall()

#         # Fetch Product data
#         cursor.execute("SELECT * FROM Product")
#         product_rows = cursor.fetchall()

#         aggregated_data = {}
#         for product in product_rows:
#             supplier_id = product[5]
#             quantity_in_stock = product[3]

#             # Find supplier details
#             supplier = next((s for s in supplier_rows if s[0] == supplier_id), None)
#             if supplier:
#                 supplier_name = supplier[1]
#                 if supplier_name in aggregated_data:
#                     aggregated_data[supplier_name] += quantity_in_stock
#                 else:
#                     aggregated_data[supplier_name] = quantity_in_stock

#         # Prepare result
#         result = [{'supplier_name': name, 'total_quantity': total} for name, total in aggregated_data.items()]

#         return result

#     except Exception as e:
#         print(f"The error '{e}' occurred")
#         raise

#     finally:
#         cursor.close()


def get_total_quantity_per_supplier_python(connection):
    try:
        cursor = connection.cursor()

        # Fetch Supplier data
        cursor.execute("SELECT * FROM Supplier")
        supplier_rows = cursor.fetchall()

        # Fetch Product data
        cursor.execute("SELECT * FROM Product")
        product_rows = cursor.fetchall()

        # Organize supplier data into a dictionary for quick lookup
        supplier_dict = {supplier[0]: supplier[1] for supplier in supplier_rows}

        # Aggregate quantities per supplier
        aggregated_data = {}
        for product in product_rows:
            supplier_id = product[5]
            quantity_in_stock = product[3]

            supplier_name = supplier_dict.get(supplier_id)
            if supplier_name:
                if supplier_name in aggregated_data:
                    aggregated_data[supplier_name] += quantity_in_stock
                else:
                    aggregated_data[supplier_name] = quantity_in_stock

        # Prepare result
        result = [{'supplier_name': name, 'total_quantity': total} for name, total in aggregated_data.items()]

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

# ORDER BY / sort

def sort_employees_by_name(employees):
    # Sort employees by name (Python-based sorting)
    return sorted(employees, key=lambda emp: emp[1])  # Assuming employee name is in the second column

