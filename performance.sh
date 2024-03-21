#!/bin/bash

echo -e "Welcome!\n"
echo -e "A series of tests will be conducted. Each Application Layer will be tested against the different Data Layers and datasets.\n"

# Define name of output file
file="results.csv"

# Check if file exists and write headers if not
if [ ! -f "$file" ]; then
    echo "Test Number,Data Layer,Application Layer,Test,Name Lookup,Connect,App Connect,PreTransfer,Redirect,Start Transfer,Total Time" > "$file"
fi

# Test Python (Flask)
./python-tests.sh

countdown_seconds=20

echo "Waiting for new tests for $countdown_seconds seconds..."

while [ $countdown_seconds -gt 0 ]; do
    echo "$countdown_seconds seconds remaining..."
    sleep 1
    ((countdown_seconds--))
done

echo -e "Countdown complete!\n"

# Test JavaScript (Node.js)
./javascript-tests.sh

docker compose down --rmi