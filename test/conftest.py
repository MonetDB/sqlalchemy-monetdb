from sqlalchemy.dialects import registry

registry.register("monetdb", "sqlalchemy_monetdb.dialect", "MonetDialect")
#regisry.register("monetdb+lite", "sqlalchemy_monetdb.dialect_lite", "MonetLiteDialect")

from sqlalchemy.testing.plugin.pytestplugin import *
