from collections.abc import Sequence
from typing import Optional
from typing import TYPE_CHECKING
from typing import overload


from sqlalchemy.sql import sqltypes as sqltypes
from sqlalchemy.types import (
    INTEGER,
    BIGINT,
    SMALLINT,
    VARCHAR,
    CHAR,
    TEXT,
    FLOAT,
    DATE,
    BOOLEAN,
    DECIMAL,
    TIMESTAMP,
    BLOB,
    JSON,
    UUID,
)
from uuid import UUID as _python_UUID


class INET(sqltypes.TypeEngine):
    __visit_name__ = "INET"


class URL(sqltypes.TypeEngine):
    __visit_name__ = "URL"


class WRD(sqltypes.Integer):
    __visit_name__ = "WRD"


class DOUBLE_PRECISION(sqltypes.Float):
    __visit_name__ = "DOUBLE_PRECISION"


class TINYINT(sqltypes.Integer):
    __visit_name__ = "TINYINT"


class TIME(sqltypes.TIME):
    """MonetDB TIME type."""

    __visit_name__ = "TIME"

    def __init__(self, timezone: bool = False, precision: Optional[int] = None) -> None:
        """Construct a TIME.

        :param timezone: boolean value if timezone present, default False
        :param precision: optional integer precision value

         .. versionadded:: 2.0

        """
        super().__init__(timezone=timezone)
        self.precision = precision
        print("time self", precision)


class MDB_JSON(sqltypes.JSON):
    __visit_name__ = "JSON"


class JSONPathType(sqltypes.JSON.JSONPathType):
    def _processor(self, dialect, super_proc):
        def process(value):
            if issubclass(type(value), Sequence):
                value = "$%s" % (
                    "".join(
                        [
                            "[%s]" % e if isinstance(e, int) else '.%s' % e
                            for e in value
                        ]
                    )
                )
            elif isinstance(value, str):
                return value
            else:
                value = "{}"
            if super_proc:
                value = super_proc(value)

            return value

        return process

    def bind_processor(self, dialect):
        return self._processor(dialect, self.string_bind_processor(dialect))

    def literal_processor(self, dialect):
        return self._processor(dialect, self.string_literal_processor(dialect))


class JSONPATH(JSONPathType):
    __visit_name__ = "JSONPATH"


class MDB_UUID(sqltypes.UUID[sqltypes._UUID_RETURN]):
    render_bind_cast = True
    render_literal_cast = True

    if TYPE_CHECKING:

        @overload
        def __init__(
            self: MDB_UUID[_python_UUID], as_uuid: Literal[True] = ...
        ) -> None:
            ...

        @overload
        def __init__(self: MDB_UUID[str], as_uuid: Literal[False] = ...) -> None:
            ...

        def __init__(self, as_uuid: bool = True) -> None:
            ...


MONETDB_TYPE_MAP = {
    "tinyint": TINYINT,
    "wrd": WRD,
    "url": URL,
    "inet": INET,
    "bigint": BIGINT,
    "blob": BLOB,
    "boolean": BOOLEAN,
    "char": CHAR,
    "clob": TEXT,
    "date": DATE,
    "decimal": DECIMAL,
    "double": DOUBLE_PRECISION,
    "int": INTEGER,
    "real": FLOAT,
    "smallint": SMALLINT,
    "time": TIME,
    "timetz": TIME,
    "timestamp": TIMESTAMP,
    "timestamptz": TIMESTAMP,
    "varchar": VARCHAR,
    "uuid": MDB_UUID,
    "json": MDB_JSON,
}
