#!/usr/bin/env python3

import logging
import sys
import pymonetdb
logging.basicConfig(level=logging.DEBUG)

db_name_or_url = sys.argv[1]

conn = pymonetdb.connect(database=db_name_or_url)
cursor = conn.cursor()
cursor.execute("CREATE SCHEMA test_schema")
cursor.execute("CREATE SCHEMA test_schema2")
cursor.execute("ALTER USER monetdb SET SCHEMA test_schema2")
conn.commit()
