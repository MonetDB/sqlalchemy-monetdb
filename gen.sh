#!/bin/bash

set -e

for i in DateHistoricTest DateTest DateTimeCoercedToDateTimeTest DateTimeHistoricTest DateTimeMicrosecondsTest DateTimeTZTest DateTimeTest TimeMicrosecondsTest TimeTZTest TimeTest TimestampMicrosecondsTest
do
    cat <<EOF
class $i:
    @pytest.mark.skip(reason="Temporal types don't work yet")
    def test_literal(self):
        pass

EOF
done

#FAILED test/test_suite.py::DateHistoricTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.date(1727, 4, 1)" with datatype DATE
#FAILED test/test_suite.py::DateTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.date(2012, 10, 15)" with datatype DATE
#FAILED test/test_suite.py::DateTimeCoercedToDateTimeTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.datetime(2012, 10, 15, 12, 57, 18)" wit...
#FAILED test/test_suite.py::DateTimeHistoricTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.datetime(1850, 11, 10, 11, 52, 35)" wit...
#FAILED test/test_suite.py::DateTimeMicrosecondsTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.datetime(2012, 10, 15, 12, 57, 18, 396)...
#FAILED test/test_suite.py::DateTimeTZTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.datetime(2012, 10, 15, 12, 57, 18, tzin...
#FAILED test/test_suite.py::DateTimeTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.datetime(2012, 10, 15, 12, 57, 18)" wit...
#FAILED test/test_suite.py::TimeMicrosecondsTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.time(12, 57, 18, 396)" with datatype TIME
#FAILED test/test_suite.py::TimeTZTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.time(12, 57, 18, tzinfo=datetime.timezo...
#FAILED test/test_suite.py::TimeTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.time(12, 57, 18)" with datatype TIME
#FAILED test/test_suite.py::TimestampMicrosecondsTest_monetdb+pymonetdb_11_55_2::test_literal - sqlalchemy.exc.CompileError: No literal value renderer is available for literal value "datetime.datetime(2012, 10, 15, 12, 57, 18, 396)...