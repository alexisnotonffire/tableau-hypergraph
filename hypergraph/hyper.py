from tableauhyperapi import Connection, CreateMode, HyperProcess, Telemetry
from tableauhyperapi.inserter import Inserter
from tableauhyperapi.sqltype import SqlType
from tableauhyperapi.tabledefinition import TableDefinition
from tableauhyperapi.tablename import TableName
import os


class HyperCreator:
    """Creates a Hyper extract file from provided schema and provides method to populate it"""

    def __init__(self, schema, file_path):
        """Initializes HyperCreator

        Args:
            schema: YAML file containing the desired schema format and queries
            file_path: Path to save the extract to
        """
        build_dir, _ = os.path.split(file_path)
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        self.hyper = file_path
        self.schema = schema
        self.tables = self._define_tables()
        self.table_names = [table.table_name.name.unescaped for table in self.tables]

        self._create_schema()

    def _define_tables(self):
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

    def _create_schema(self):
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(
                hyper.endpoint, self.hyper, CreateMode.CREATE_AND_REPLACE
            ) as connection:
                for table in self.tables:
                    connection.catalog.create_table(table)

    def populate_extract(self, table, data):
        """Connect to Hyper file and load table with data

        Args:
            table: name of the table you are loading
            data: iterable object containing data to populate table with
        """
        if not any(table == name for name in self.table_names):
            raise ValueError(f"{table} is not part of the schema")

        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(hyper.endpoint, self.hyper) as connection:
                with Inserter(connection, table) as inserter:
                    inserter.add_rows(data)
                    inserter.execute()
