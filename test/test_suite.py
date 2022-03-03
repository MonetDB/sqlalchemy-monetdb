from distutils.command.config import config
import sqlalchemy as sa
from sqlalchemy.testing.assertions import AssertsCompiledSQL, AssertsExecutionResults
from sqlalchemy.testing.suite import *
from sqlalchemy.testing.suite import ComponentReflectionTest as _ComponentReflectionTest
from sqlalchemy.testing.suite import ExceptionTest as _ExceptionTest
from sqlalchemy.testing.suite import OrderByLabelTest as _OrderByLabelTest
from sqlalchemy import inspect
from sqlalchemy.testing import fixtures, eq_, is_
from sqlalchemy import testing
from sqlalchemy.schema import DDL, Index
from sqlalchemy import event
from sqlalchemy import MetaData
from sqlalchemy.sql.expression import literal

import sqlalchemy_monetdb.monetdb_types as mtypes


major, minor = [int(i) for i in sa.__version__.split('.')[:2]]


class ComponentReflectionTest(_ComponentReflectionTest):
    def __init__(self) -> None:
        with config.db.connection as conn:
            conn.execute("DROP SCHEMA test_schema2 CASCADE")
            conn.execute("DROP SCHEMA test_schema CASCADE")
            conn.execute("CREATE SCHEMA test_schema2")
            conn.execute("CREATE SCHEMA test_schema")
        super().__init__()


    @testing.requires.foreign_key_constraint_reflection
    def test_get_foreign_keys(self):
        """we use test_schema2 schema"""
        self._test_get_foreign_keys(schema='test_schema2')

    @testing.requires.temp_table_reflection
    def test_get_temp_table_columns(self):
        """In MonetDB temp tables have the tmp schema, so the name is tmp.user_tmp"""
        meta = MetaData(self.bind)
        user_tmp = self.tables['tmp.user_tmp']
        insp = inspect(meta.bind)
        cols = insp.get_columns('user_tmp', schema='tmp')
        self.assert_(len(cols) > 0, len(cols))

        for i, col in enumerate(user_tmp.columns):
            eq_(col.name, cols[i]['name'])

    @testing.requires.temp_table_reflection
    def test_get_temp_table_indexes(self):
        # TODO: it looks like MonetDB doesn't show index for temp tables (yet)
        pass

    @testing.requires.temp_table_reflection
    @testing.requires.unique_constraint_reflection
    def test_get_temp_table_unique_constraints(self):
        # TODO: it looks like MonetDB doesn't show constrains for temp tables (yet)
        return

    @classmethod
    def define_temp_tables(cls, metadata):
        user_tmp = Table(
            "user_tmp", metadata,
            Column("id", sa.INT, primary_key=True),
            Column('name', sa.VARCHAR(50)),
            Column('foo', sa.INT),
            sa.UniqueConstraint('name', name='user_tmp_uq'),
            sa.Index("user_tmp_ix", "foo"),
            prefixes=["TEMPORARY"],
            schema='tmp',
        )
        if testing.requires.view_reflection.enabled and \
                testing.requires.temporary_views.enabled:
            event.listen(
                user_tmp, "after_create",
                DDL("create view user_tmp_v as "
                    "select * from tmp.user_tmp")
            )
            event.listen(
                user_tmp, "before_drop",
                DDL("drop view user_tmp_v")
            )

    @classmethod
    def define_reflected_tables(cls, metadata, schema):
        if major >= 1 and minor >= 2:
            cls._define_reflected_tables_12(metadata, schema)
        else:
            super(ComponentReflectionTest, cls).define_reflected_tables(metadata, schema)

    @classmethod
    def _define_reflected_tables_12(cls, metadata, schema):
        if schema:
            schema_prefix = schema + "."
        else:
            schema_prefix = ""

        if testing.requires.self_referential_foreign_keys.enabled:
            users = Table('users', metadata,
                          Column('user_id', sa.INT, primary_key=True),
                          Column('test1', sa.CHAR(5), nullable=False),
                          Column('test2', sa.Float(5), nullable=False),
                          Column('parent_user_id', sa.Integer,
                                 sa.ForeignKey('%susers.user_id' %
                                               "test_schema.",
                                               name='user_id_fk')),
                          schema=schema,
                          test_needs_fk=True,
                          )
        else:
            users = Table('users', metadata,
                          Column('user_id', sa.INT, primary_key=True),
                          Column('test1', sa.CHAR(5), nullable=False),
                          Column('test2', sa.Float(5), nullable=False),
                          schema=schema,
                          test_needs_fk=True,
                          )

        Table("dingalings", metadata,
              Column('dingaling_id', sa.Integer, primary_key=True),
              Column('address_id', sa.Integer,
                     sa.ForeignKey('%semail_addresses.address_id' %
                                   schema_prefix)),
              Column('data', sa.String(30)),
              schema=schema,
              test_needs_fk=True,
              )
        Table('email_addresses', metadata,
              Column('address_id', sa.Integer),
              Column('remote_user_id', sa.Integer,
                     sa.ForeignKey(users.c.user_id)),
              Column('email_address', sa.String(20)),
              sa.PrimaryKeyConstraint('address_id', name='email_ad_pk'),
              schema=schema,
              test_needs_fk=True,
              )
        Table('comment_test', metadata,
              Column('id', sa.Integer, primary_key=True, comment='id comment'),
              Column('data', sa.String(20), comment='data % comment'),
              Column(
                  'd2', sa.String(20),
                  comment=r"""Comment types type speedily ' " \ '' Fun!"""),
              schema=schema,
              comment=r"""the test % ' " \ table comment""")

        if testing.requires.index_reflection.enabled:
            cls.define_index(metadata, users)

            if not schema:
                noncol_idx_test_nopk = Table(
                    'noncol_idx_test_nopk', metadata,
                    Column('q', sa.String(5)),
                )
                noncol_idx_test_pk = Table(
                    'noncol_idx_test_pk', metadata,
                    Column('id', sa.Integer, primary_key=True),
                    Column('q', sa.String(5)),
                )
                Index('noncol_idx_nopk', noncol_idx_test_nopk.c.q)
                Index('noncol_idx_pk', noncol_idx_test_pk.c.q)

        if testing.requires.view_column_reflection.enabled:
            cls.define_views(metadata, schema)
        if not schema and testing.requires.temp_table_reflection.enabled:
            cls.define_temp_tables(metadata)

    @testing.requires.index_reflection
    def test_get_noncol_index_pk(self):
        # TODO: not working for now?
        return

        tname = "noncol_idx_test_nopk"
        ixname = "noncol_idx_nopk"
        meta = self.metadata
        insp = inspect(meta.bind)
        indexes = insp.get_indexes(tname)

        # reflecting an index that has "x DESC" in it as the column.
        # the DB may or may not give us "x", but make sure we get the index
        # back, it has a name, it's connected to the table.
        expected_indexes = [
            {'unique': False,
             'name': ixname}
        ]
        self._assert_insp_indexes(indexes, expected_indexes)

        t = Table(tname, meta, autoload_with=meta.bind)
        eq_(len(t.indexes), 2)
        is_(list(t.indexes)[0].table, t)
        eq_(list(t.indexes)[0].name, ixname)


class ExceptionTest(_ExceptionTest):
    """
    overriding this since a bug in test suite:

    https://gerrit.sqlalchemy.org/#/c/576/
    """
    @requirements.duplicate_key_raises_integrity_error
    def test_integrity_error(self):

        def inner():
            with config.db.begin() as conn:
                conn.execute(self.tables.manual_pk.insert(), {'id': 1, 'data': 'd1'})
                conn.execute(self.tables.manual_pk.insert(), {'id': 1, 'data': 'd1'})

        assert_raises(
            exc.IntegrityError,
            inner
        )


class OrderByLabelTest(_OrderByLabelTest):
    def test_group_by_composed(self):
        """
        Disable this for now

        https://github.com/gijzelaerr/sqlalchemy-monetdb/issues/21
        https://groups.google.com/forum/#!topic/sqlalchemy/r4X7ddN4rgA
        """
        pass


class CompileTest(fixtures.TestBase, AssertsCompiledSQL):

    def test_ne_operator(self):

        self.assert_compile(
            literal(5) != literal(10),
            '%(param_1)s <> %(param_2)s',
            checkparams={'param_1': 5, 'param_2': 10}
        )


class TypesTest(fixtures.TestBase, AssertsCompiledSQL):

    def test_numeric(self):
        columns = [
            # column type, args, kwargs, expected ddl
            (mtypes.TINYINT, [], {}, 'TINYINT'),
        ]

        for type_, args, kw, res in columns:
            type_inst = type_(*args, **kw)

            self.assert_compile(
                type_inst,
                res
            )
