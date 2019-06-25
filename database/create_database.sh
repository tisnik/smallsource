#!/bin/sh

DATABASE=smallsource.db

cat schema.sql | sqlite3 ../workdir/${DATABASE}
cat test_data.sql | sqlite3 ../workdir/${DATABASE}

