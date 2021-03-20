from hypergraph.datasource import Datasource
from hypergraph.graphql import GraphQL
from hypergraph.hyper import HyperCreator
from hypergraph.tableau import Tableau
import yaml

CONTENT_MANAGEMENT = "resources/content_management"
SCHEMA_FILE = "resources/content_management/schema.yaml"
HYPER_FILE = "build/tableau.hyper"
TDSX_FILE = "resources/hypergraph.tdsx"
TOKEN_FILE = "resources/token"


def create_extract():
    """Create HYPER_FILE from SCHEMA_FILE and load with metadata query results"""
    with open(SCHEMA_FILE, "r") as f:
        SCHEMA = yaml.safe_load(f)

    with open(TOKEN_FILE, "r") as f:
        TOKEN = yaml.safe_load(f)

    hc = HyperCreator(SCHEMA, HYPER_FILE)
    ts = Tableau(TOKEN["server"], TOKEN["site"], TOKEN["name"], TOKEN["value"])

    for table in SCHEMA["tables"]:
        with open(f"{CONTENT_MANAGEMENT}/{table['query']}", "r") as f:
            query = f.read()

        data = ts.query_metadata(query)
        data_map = getattr(GraphQL, table["name"])(data)

        hc.populate_extract(table["name"], data_map)


def update_datasource():
    """Replace current extract in TDSX_FILE with HYPER_FILE"""
    ds = Datasource(TDSX_FILE)
    ds.replace_extract(HYPER_FILE)


def main():
    create_extract()
    update_datasource()


if __name__ == "__main__":
    main()