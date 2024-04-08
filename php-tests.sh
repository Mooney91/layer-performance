#!/bin/bash

# Testing PHP
echo -e "\nPHP will now be tested.\n"

datasets=(
    ./MySQL/10000
    ./MySQL/50000
    ./MySQL/100000
)

count=1

file="results.csv"

function test_mysql() {  
    for i in {1..100}
    do
        echo -e "Round: ${i}"
        # docker compose up data-mysql --force-recreate --detach --wait
        # docker compose up app-php --force-recreate --detach --wait

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

        # docker compose down app-php
        # docker compose down data-mysql
    done
}

for dataset in "${datasets[@]}"; do

    export MYSQL_DATASET=$dataset

    docker compose up data-mysql --force-recreate --detach --wait
    docker compose up app-php --force-recreate --detach --wait

    sleep 20

    echo -e "Testing: php-mysql-data-aggre-$count"
    test_mysql "MySQL" "php" "php-mysql-data-aggre-$count" "http://127.0.0.1:1338/aggregation-mysql" "$file"

    echo -e "Testing: php-mysql-app-aggre-$count"
    test_mysql "MySQL" "php" "php-mysql-app-aggre-$count" "http://127.0.0.1:1338/aggregation-php" "$file"

    echo -e "Testing: php-mysql-data-filter-$count"
    test_mysql "MySQL" "php" "php-mysql-data-filter-$count" "http://127.0.0.1:1338/filter-mysql" "$file"

    echo -e "php-mysql-app-filter-$count"
    test_mysql "MySQL" "php" "php-mysql-app-filter-$count" "http://127.0.0.1:1338/filter-php" "$file"

    echo -e "Testing: php-mysql-data-sort-$count"
    test_mysql "MySQL" "php" "php-mysql-data-sort-$count" "http://127.0.0.1:1338/sorting-mysql" "$file"

    echo -e "Testing: php-mysql-app-sort-$count"
    test_mysql "MySQL" "php" "php-mysql-app-sort-$count" "http://127.0.0.1:1338/sorting-php" "$file"

    echo -e "Testing: php-mysql-data-procedure-$count"
    test_mysql "MySQL" "php" "php-mysql-data-procedure-$count" "http://127.0.0.1:1338/procedure-mysql" "$file"

    echo -e "Testing: php-mysql-app-procedure-$count"
    test_mysql "MySQL" "php" "php-mysql-app-procedure-$count" "http://127.0.0.1:1338/procedure-php" "$file"

    echo -e "Testing: php-mysql-data-adprocedure-$count"
    test_mysql "MySQL" "php" "php-mysql-data-adprocedure-$count" "http://127.0.0.1:1338/advanced-procedure-mysql" "$file"

    echo -e "Testing: php-mysql-app-adprocedure-$count"
    test_mysql "MySQL" "php" "php-mysql-app-adprocedure-$count" "http://127.0.0.1:1338/advanced-procedure-php" "$file"

    docker compose down app-php
    docker compose down data-mysql
    docker compose down --rmi

    ((count++))  
done
