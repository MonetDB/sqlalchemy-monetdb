# import pdb
from sqlalchemy import types as sqltypes, schema, util
from sqlalchemy.sql import compiler, operators, cast

import re

FK_ON_DELETE = re.compile(
    r"^(?:RESTRICT|CASCADE|SET NULL|NO ACTION|SET DEFAULT)$", re.I
)
FK_ON_UPDATE = re.compile(
    r"^(?:RESTRICT|CASCADE|SET NULL|NO ACTION|SET DEFAULT)$", re.I
)


class MonetDDLCompiler(compiler.DDLCompiler):
    def visit_create_sequence(self, create, **kwargs):
        text = "CREATE SEQUENCE %s AS INTEGER" % self.preparer.format_sequence(
            create.element
        )
        if create.element.start is not None:
            text += " START WITH %d" % create.element.start
        if create.element.increment is not None:
            text += " INCREMENT BY %d" % create.element.increment
        return text

    def visit_drop_sequence(self, drop, **kwargs):
        return "DROP SEQUENCE %s" % self.preparer.format_sequence(drop.element)

    def define_constraint_cascades(self, constraint):
        text = ""
        text += " ON DELETE %s" % self.preparer.validate_sql_phrase(
            constraint.ondelete if constraint.ondelete else "NO ACTION", FK_ON_DELETE
        )
        text += " ON UPDATE %s" % self.preparer.validate_sql_phrase(
            constraint.onupdate if constraint.onupdate else "NO ACTION", FK_ON_UPDATE
        )
        return text

    def visit_identity_column(self, identity, **kw):
        text = "GENERATED %s AS IDENTITY" % (
            "ALWAYS",  # if identity.always else "BY DEFAULT",
        )
        options = self.get_identity_options(identity)
        if options:
            text += " (%s)" % options
        return text

    def get_column_specification(self, column, **kwargs):
        colspec = self.preparer.format_column(column)
        impl_type = column.type.dialect_impl(self.dialect)
        if (
            column.primary_key
            and column is column.table._autoincrement_column
            and column.identity is None
            and not isinstance(impl_type, sqltypes.SmallInteger)
            and (
                column.default is None
                or (
                    isinstance(column.default, schema.Sequence)
                    and column.default.optional
                )
            )
        ):
            colspec += " INT AUTO_INCREMENT"
        else:
            colspec += " " + self.dialect.type_compiler.process(column.type)
            default = self.get_column_default_string(column)
            if default is not None:
                colspec += " DEFAULT " + default

        if column.identity:
            colspec += " " + self.process(column.identity)

        if not column.nullable:
            colspec += " NOT NULL"
        return colspec

    def visit_create_index(self, create, **kw):
        preparer = self.preparer
        index = create.element
        if index.unique:
            text = "ALTER TABLE %s ADD CONSTRAINT %s UNIQUE " % (
                preparer.format_table(index.table),
                self._prepared_index_name(index, include_schema=False),
            )
        else:
            text = "CREATE "
            text += "INDEX "

            if create.if_not_exists:
                text += "IF NOT EXISTS "

            text += "%s ON %s " % (
                self._prepared_index_name(index, include_schema=False),
                preparer.format_table(index.table),
            )

        if len(index.expressions) > 0:
            text += " (%s)" % ", ".join(
                self.sql_compiler.process(expr, include_table=False, literal_binds=True)
                for expr in index.expressions
            )

        return text


class MonetTypeCompiler(compiler.GenericTypeCompiler):
    def visit_DOUBLE_PRECISION(self, type_):
        return "DOUBLE PRECISION"

    def visit_INET(self, type_):
        return "INET"

    def visit_URL(self, type_):
        return "URL"

    def visit_WRD(self, type_):
        return "WRD"

    def visit_TINYINT(self, type_):
        return "TINYINT"

    def visit_datetime(self, type_, **kwargs):
        return self.visit_TIMESTAMP(type_)

    def visit_TIMESTAMP(self, type_, **kwargs):
        if type_.timezone:
            return "TIMESTAMP WITH TIME ZONE"
        return "TIMESTAMP"

    def visit_TIME(self, type_, **kw):
        return "TIME%s %s" % (
            "(%d)" % type_.precision
            if getattr(type_, "precision", None) is not None
            else "(6)",
            (type_.timezone and "WITH" or "WITHOUT") + " TIME ZONE",
        )

    def visit_VARCHAR(self, type_, **kwargs):
        if type_.length is None:
            return "CLOB"
        return compiler.GenericTypeCompiler.visit_VARCHAR(self, type_)

    def visit_uuid(self, type_, **kw):
        if type_.native_uuid:
            return self.visit_UUID(type_, **kw)
        else:
            return super().visit_uuid(type_, **kw)

    def visit_UUID(self, type_, **kw):
        return "UUID"

    def visit_JSON(self, type_, **kw):
        return "JSON"

    def visit_JSONPath(self, type_, **kw):
        return "JSONPATH"


class MonetCompiler(compiler.SQLCompiler):
    # MonetDB only allowes simple names (strings) as parameters names
    # Some remapping is done here
    bindname_escape_characters = util.immutabledict(
        {
            "%": "P",
            "(": "A",
            ")": "Z",
            ":": "C",
            ".": "C",
            "[": "C",
            "]": "C",
            " ": "C",
            "\\": "C",
            "/": "C",
            "?": "C",
        }
    )

    def bindparam_string(self, name, **kw):
        if self.preparer._bindparam_requires_quotes(name) and not kw.get(
            "post_compile", False
        ):
            new_name = name
            if name[0] == "%":
                new_name = "_" + name
            quoted_name = '"%s"' % new_name
            kw["escaped_from"] = name
            name = quoted_name
            return compiler.SQLCompiler.bindparam_string(self, name, **kw)

        escaped_from = kw.get("escaped_from", None)
        if not escaped_from:
            if self._bind_translate_re.search(name):
                new_name = self._bind_translate_re.sub(
                    lambda m: self._bind_translate_chars[m.group(0)],
                    name,
                )
                if new_name[0].isdigit() or new_name[0] == "_" or new_name[0] == "%":
                    new_name = "D" + new_name
                kw["escaped_from"] = name
                name = new_name
            elif name[0].isdigit() or name[0] == "_" or name[0] == "%":
                new_name = "D" + name
                kw["escaped_from"] = name
                name = new_name

        return compiler.SQLCompiler.bindparam_string(self, name, **kw)

    def visit_mod(self, binary, **kw):
        return self.process(binary.left) + " %% " + self.process(binary.right)

    def visit_sequence(self, seq, **kwargs):
        exc = "(NEXT VALUE FOR %s)" % self.dialect.identifier_preparer.format_sequence(
            seq
        )
        return exc

    def limit_clause(self, select, **kw):
        text = ""
        if select._limit_clause is not None:
            text += "\n LIMIT " + self.process(select._limit_clause, **kw)
        if select._offset_clause is not None:
            text += " OFFSET " + self.process(select._offset_clause, **kw)
        return text

    def visit_extended_join(self, join, asfrom=False, **kwargs):
        """Support for full outer join, created by
        rb.data.sqlalchemy.ExtendedJoin
        """

        if join.isouter and join.isfullouter:
            join_type = " FULL OUTER JOIN "
        elif join.isouter:
            join_type = " LEFT OUTER JOIN "
        else:
            join_type = " JOIN "

        return (
            join.left._compiler_dispatch(self, asfrom=True, **kwargs)
            + join_type
            + join.right._compiler_dispatch(self, asfrom=True, **kwargs)
            + " ON "
            + join.onclause._compiler_dispatch(self, **kwargs)
        )

    def visit_ne(self, element, **kwargs):
        return (
            element.left._compiler_dispatch(self, **kwargs)
            + " <> "
            + element.right._compiler_dispatch(self, **kwargs)
        )

    def render_literal_value(self, value, type_):
        # we need to escape backslashes
        value = super(MonetCompiler, self).render_literal_value(value, type_)
        return value.replace("\\", "\\\\")

    def update_from_clause(
        self, update_stmt, from_table, extra_froms, from_hints, **kw
    ):
        return "FROM " + ", ".join(
            t._compiler_dispatch(self, asfrom=True, fromhints=from_hints, **kw)
            for t in extra_froms
        )

    def visit_empty_set_op_expr(self, type_, expand_op, **kw):
        if expand_op is operators.not_in_op:
            if len(type_) > 1:
                return "(%s)) OR (1 = 1" % (", ".join("NULL" for element in type_))
            else:
                return "NULL) OR (1 = 1"
        elif expand_op is operators.in_op:
            if len(type_) > 1:
                return "(%s)) AND (1 <> 1" % (", ".join("NULL" for element in type_))
            else:
                return "NULL) AND (1 <> 1"
        else:
            return self.visit_empty_set_expr(type_)

    def visit_empty_set_expr(self, element_types, **kw):
        # cast the empty set to the type we are comparing against.  if
        # we are comparing against the null type, pick an arbitrary
        # datatype for the empty set
        return "SELECT %s WHERE 1<>1" % (
            ", ".join(
                "CAST(NULL AS %s)"
                % self.dialect.type_compiler_instance.process(
                    sqltypes.INTEGER() if type_._isnull else type_
                )
                for type_ in element_types or [sqltypes.INTEGER()]
            ),
        )

    def visit_like_op_binary(self, binary, operator, **kw):
        escape = binary.modifiers.get("escape", None)

        res = "%s LIKE %s" % (
            binary.left._compiler_dispatch(self, **kw),
            binary.right._compiler_dispatch(self, **kw),
        ) + (
            " ESCAPE " + self.render_literal_value(escape, sqltypes.STRINGTYPE)
            if escape is not None
            else ""
        )

        return res

    def _regexp_match(self, base_op, binary, operator, kw):
        flags = binary.modifiers["flags"]
        if flags is None:
            return self._generate_generic_binary(binary, " %s " % base_op, **kw)
        if flags == "i":
            return self._generate_generic_binary(binary, " %s* " % base_op, **kw)
        return "%s %s CONCAT('(?', %s, ')', %s)" % (
            self.process(binary.left, **kw),
            base_op,
            self.render_literal_value(flags, sqltypes.STRINGTYPE),
            self.process(binary.right, **kw),
        )

    def visit_regexp_match_op_binary(self, binary, operator, **kw):
        return self._regexp_match("~", binary, operator, kw)

    def visit_not_regexp_match_op_binary(self, binary, operator, **kw):
        return self._regexp_match("!~", binary, operator, kw)

    def visit_regexp_replace_op_binary(self, binary, operator, **kw):
        string = self.process(binary.left, **kw)
        pattern_replace = self.process(binary.right, **kw)
        flags = binary.modifiers["flags"]
        if flags is None:
            return "REGEXP_REPLACE(%s, %s)" % (
                string,
                pattern_replace,
            )
        else:
            return "REGEXP_REPLACE(%s, %s, %s)" % (
                string,
                pattern_replace,
                self.render_literal_value(flags, sqltypes.STRINGTYPE),
            )

    def _render_json_extract_from_binary(self, binary, operator, _cast_applied=False, **kw):
        if (
            not _cast_applied
            and binary.type._type_affinity is not sqltypes.JSON
        ):
            kw["_cast_applied"] = True
            return self.process(cast(binary, binary.type), **kw)

        left = self.process(binary.left, **kw)
        right = self.process(binary.right, **kw)
        if binary.type._type_affinity is sqltypes.JSON:
            return "JSON.FILTER(%s, %s)" % (left, right)
        else:
            return "CASE JSON.FILTER(%s, %s) WHEN 'null' THEN NULL ELSE JSON.TEXT(JSON.FILTER(%s, %s)) END" % (left, right, left, right)

    def visit_json_getitem_op_binary(self, binary, operator, _cast_applied=False, **kw):
        return self._render_json_extract_from_binary(binary, operator, _cast_applied, **kw)

    def visit_json_path_getitem_op_binary(self, binary, operator, _cast_applied=False, **kw):
        return self._render_json_extract_from_binary(binary, operator, _cast_applied, **kw)
