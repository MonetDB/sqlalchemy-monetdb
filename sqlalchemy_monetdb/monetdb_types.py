from sqlalchemy import types as sqltypes
from sqlalchemy.types import INTEGER, BIGINT, SMALLINT, VARCHAR, CHAR, TEXT,\
    FLOAT, DATE, BOOLEAN, DECIMAL, TIMESTAMP, TIME, BLOB


class INET(sqltypes.TypeEngine):
    __visit_name__ = "INET"


class URL(sqltypes.TypeEngine):
    __visit_name__ = "URL"


class WRD(sqltypes.Integer):
    __visit_name__ = "WRD"


class DOUBLE_PRECISION(sqltypes.Float):
    __visit_name__ = 'DOUBLE_PRECISION'


class TINYINT(sqltypes.Integer):
    __visit_name__ = "TINYINT"


MONETDB_TYPE_MAP = {
    'tinyint': TINYINT,
    'wrd': WRD,
    'url': URL,
    'inet': INET,
    'bigint': BIGINT,
    'blob': BLOB,
    'boolean': BOOLEAN,
    'char': CHAR,
    'clob': TEXT,
    'date': DATE,
    'decimal': DECIMAL,
    'double': DOUBLE_PRECISION,
    'int': INTEGER,
    'real': FLOAT,
    'smallint': SMALLINT,
    'time': TIME,
    'timestamp': TIMESTAMP,
    'timestamptz': TIMESTAMP,
    'varchar': VARCHAR,
}
