from tableauhyperapi import Connection, CreateMode, HyperProcess, Telemetry
from tableauhyperapi.inserter import Inserter
from tableauhyperapi.sqltype import SqlType
from tableauhyperapi.tabledefinition import TableDefinition
from tableauhyperapi.tablename import TableName


class HyperCreator:
    def __init__(self, schema, hyper_file=None):
        self.schema = schema
        self.hyper = hyper_file or "build/extract.hyper"
        self.tables = self.define_tables()
        self.table_names = [table.table_name.name.unescaped for table in self.tables]

        self.create_schema()

    def define_tables(self):
        tables = []
        for table in self.schema["tables"]:
            tables.append(
                TableDefinition(
                    TableName(table["name"]),
                    [
                        TableDefinition.Column(c["name"], getattr(SqlType, c["type"])())
                        for c in table["fields"]
                    ],
                )
            )

        return tables

    def create_schema(self):
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(
                hyper.endpoint, self.hyper, CreateMode.CREATE_AND_REPLACE
            ) as connection:
                for table in self.tables:
                    connection.catalog.create_table(table)
                    print(f"created table: {table.table_name}")

    def populate_extract(self, table, data):
        if not any(table == name for name in self.table_names):
            raise ValueError(f"{table} is not part of the schema")

        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(hyper.endpoint, self.hyper) as connection:
                with Inserter(connection, table) as inserter:
                    inserter.add_rows(data)
                    inserter.execute()
