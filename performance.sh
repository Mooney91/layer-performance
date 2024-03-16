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

docker compose down --rmi