#!/bin/sh

DATABASE=smallsource.db

sqlite3 ../workdir/${DATABASE} "vacuum"

