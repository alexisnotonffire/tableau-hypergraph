from typing import Dict
from tableauhyperapi import Connection, CreateMode, HyperProcess, Telemetry
from tableauhyperapi.inserter import Inserter
from tableauhyperapi.sqltype import SqlType
from tableauhyperapi.tabledefinition import TableDefinition
from tableauhyperapi.tablename import TableName
import yaml

class HyperCreator:
    def __init__(self, schema_file, hyper_file=None):
        self._schema = yaml.safe_load(schema_file)
        self._hyper = hyper_file or "build/extract.hyper"
        
        self._create_schema(self._hyper, self._schema)


    def _define_tables(self):
        tables = []
        for table, columns in self._schema:
            tables.append(
                TableDefinition(
                    TableName(table),
                    [
                        TableDefinition.Column(
                            c.name, 
                            getattr(SqlType, c.type)()
                        )
                        for c in columns
                    ]
                )
            )

        return tables

    def _create_schema(self):
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(hyper.endpoint, self._hyper, CreateMode.CREATE_AND_REPLACE) as connection:
                for table in self._define_tables():
                    connection.catalog.create_table(table)

    def populate_extract(self, table, data):
        with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
            with Connection(hyper.endpoint, self._hyper, CreateMode.CREATE_AND_REPLACE) as connection:
                with Inserter(connection, table) as inserter:
                    inserter.add_rows(data)