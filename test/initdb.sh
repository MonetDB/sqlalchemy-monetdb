#!/usr/bin/bash
#

set -x
set -e

DATABASE="test"
USER="monetdb"
PASSWORD=${USER}

echo -en "user=${USER}\npassword=${PASSWORD}\n" > ~/.monetdb


monetdb stop $DATABASE || true
monetdb destroy -f $DATABASE || true
monetdb create $DATABASE
monetdb release $DATABASE
monetdb start $DATABASE
echo "create schema test_schema;" | mclient -d $DATABASE
echo "create schema test_schema2;" | mclient -d $DATABASE
echo "alter user monetdb set schema test_schema2;" | mclient -d $DATABASE

set +e
set +x
