#!/bin/bash

# Testing Python (Flask)
echo -e "\nPython (Flask) will now be tested.\n"

docker compose up data-mysql --force-recreate --detach --wait
docker compose up app-python --force-recreate --detach --wait

sleep 20

function test_mysql() {  
    for i in {1..10}
    do
        echo -e "Round: ${i}"
        # docker compose up data-mysql --force-recreate --detach --wait
        # docker compose up app-python --force-recreate --detach --wait

        # Execute curl and get the times
        times=$(curl -w "@csv-format.txt" -o /dev/null -s "$4")

        # Get the last test number and increment it
        last_test_number=$(tail -n 1 "$5" | cut -d',' -f1)

        # Check if last_test_number is a number
        if ! [[ $last_test_number =~ ^[0-9]+$ ]]
        then
            last_test_number=0
        fi
        test_number=$((last_test_number + 1))

        # Write to the file
        echo "$test_number,$1,$2,$3,$times" >> "$5"

        # docker compose down app-python
        # docker compose down data-mysql
    done
}

file="results.csv"

echo -e "Testing: python-mysql-data-aggre-1"
test_mysql "MySQL" "Python" "python-mysql-data-aggre-1" "http://127.0.0.1:5000/aggregation-mysql" "$file"

echo -e "Testing: python-mysql-app-aggre-1"
test_mysql "MySQL" "Python" "python-mysql-app-aggre-1" "http://127.0.0.1:5000/aggregation-python" "$file"

echo -e "Testing: python-mysql-data-filter-1"
test_mysql "MySQL" "Python" "python-mysql-data-filter-1" "http://127.0.0.1:5000/filter-mysql" "$file"

echo -e "python-mysql-app-filter-1"
test_mysql "MySQL" "Python" "python-mysql-app-filter-1" "http://127.0.0.1:5000/filter-python" "$file"

echo -e "Testing: python-mysql-data-sort-1"
test_mysql "MySQL" "Python" "python-mysql-data-sort-1" "http://127.0.0.1:5000/sorting-mysql" "$file"

echo -e "Testing: python-mysql-app-sort-1"
test_mysql "MySQL" "Python" "python-mysql-app-sort-1" "http://127.0.0.1:5000/sorting-python" "$file"

echo -e "Testing: python-mysql-data-procedure-1"
test_mysql "MySQL" "Python" "python-mysql-data-procedure-1" "http://127.0.0.1:5000/procedure-mysql" "$file"

echo -e "Testing: python-mysql-app-procedure-1"
test_mysql "MySQL" "Python" "python-mysql-app-procedure-1" "http://127.0.0.1:5000/procedure-python" "$file"

echo -e "Testing: python-mysql-data-adprocedure-1"
test_mysql "MySQL" "Python" "python-mysql-data-adprocedure-1" "http://127.0.0.1:5000/advanced-procedure-mysql" "$file"

echo -e "Testing: python-mysql-app-adprocedure-1"
test_mysql "MySQL" "Python" "python-mysql-app-adprocedure-1" "http://127.0.0.1:5000/advanced-procedure-python" "$file"

docker compose down app-python
docker compose down data-mysql
docker compose down --rmi
