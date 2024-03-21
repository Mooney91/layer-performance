#!/bin/bash

# Testing JavaScript (Node.js)
echo -e "\nJavaScript (Node.js) will now be tested.\n"

docker compose up data-mysql --force-recreate --detach --wait
docker compose up app-javascript --force-recreate --detach --wait

sleep 20

function test_mysql() {  
    for i in {1..10}
    do
        echo -e "Round: ${i}"
        # docker compose up data-mysql --force-recreate --detach --wait
        # docker compose up app-javascript --force-recreate --detach --wait

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

        # docker compose down app-javascript
        # docker compose down data-mysql
    done
}

file="results.csv"

techo -e "Testing: javascript-mysql-data-aggre-1"
test_mysql "MySQL" "javascript" "javascript-mysql-data-aggre-1" "http://127.0.0.1:1337/aggregation-mysql" "$file"

echo -e "Testing: javascript-mysql-app-aggre-1"
test_mysql "MySQL" "javascript" "javascript-mysql-app-aggre-1" "http://127.0.0.1:1337/aggregation-javascript" "$file"

echo -e "Testing: javascript-mysql-data-filter-1"
test_mysql "MySQL" "javascript" "javascript-mysql-data-filter-1" "http://127.0.0.1:1337/filter-mysql" "$file"

echo -e "javascript-mysql-app-filter-1"
test_mysql "MySQL" "javascript" "javascript-mysql-app-filter-1" "http://127.0.0.1:1337/filter-javascript" "$file"

echo -e "Testing: javascript-mysql-data-sort-1"
test_mysql "MySQL" "javascript" "javascript-mysql-data-sort-1" "http://127.0.0.1:1337/sorting-mysql" "$file"

echo -e "Testing: javascript-mysql-app-sort-1"
test_mysql "MySQL" "javascript" "javascript-mysql-app-sort-1" "http://127.0.0.1:1337/sorting-javascript" "$file"

echo -e "Testing: javascript-mysql-data-procedure-1"
test_mysql "MySQL" "javascript" "javascript-mysql-data-procedure-1" "http://127.0.0.1:1337/procedure-mysql" "$file"

echo -e "Testing: javascript-mysql-app-procedure-1"
test_mysql "MySQL" "javascript" "javascript-mysql-app-procedure-1" "http://127.0.0.1:1337/procedure-javascript" "$file"

echo -e "Testing: javascript-mysql-data-adprocedure-1"
test_mysql "MySQL" "javascript" "javascript-mysql-data-adprocedure-1" "http://127.0.0.1:1337/advanced-procedure-mysql" "$file"

echo -e "Testing: javascript-mysql-app-adprocedure-1"
test_mysql "MySQL" "javascript" "javascript-mysql-app-adprocedure-1" "http://127.0.0.1:1337/advanced-procedure-javascript" "$file"

docker compose down app-javascript
docker compose down data-mysql
docker compose down --rmi
