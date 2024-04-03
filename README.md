# Where is the Logic?

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Mooney91/layer-performance/badges/quality-score.png?b=main)](https://scrutinizer-ci.com/g/Mooney91/layer-performance/?branch=main)

This repo is in connection with a thesis project by Zachary Mooney. This is a comparative study of the performance of business logic between the Data and Application Layers of a Three-Tier System.

There are a series of tests that are executed to measure and compare performance (speed) of various functions performed either from the Data Layer or the Application Layer.

In addition, the database in the *Data Layer* will also be populated with three separate datasets: 1000, 50000, and 100000 row datasets.

## Data Layer
### MySQL

Add a .env file and indicate which dataset you wish to use. For example use `MYSQL_DATASET=./MySQL/10000` if you want to the database with 10000 rows in each table.

In bash you can also indicate the environmental variable by executing `export MYSQL_DATASET=./MySQL/10000`

## Application Layer

- Node.js
- Python
- PHP

## Running the Tests

The test suite uses Docker, so please ensure that *Docker Desktop* is up and running before you begin.

Then execute `./performance.sh`