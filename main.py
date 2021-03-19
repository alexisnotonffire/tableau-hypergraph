from hypergraph.graphql import GraphQL
from hypergraph.hyper import HyperCreator
from hypergraph.tableau import Tableau
import yaml

CONTENT_MANAGEMENT = "./resources/content_management/{}"
SCHEMA_FILE = "./resources/content_management/schema.yaml"
BUILD_DIR = "build"
HYPER_FILE = "tableau.hyper"
TOKEN_FILE = "./resources/token"

with open(SCHEMA_FILE, "r") as f:
    SCHEMA = yaml.safe_load(f)

with open(TOKEN_FILE, "r") as f:
    TOKEN = yaml.safe_load(f)

hc = HyperCreator(SCHEMA, BUILD_DIR, HYPER_FILE)
ts = Tableau(TOKEN["server"], TOKEN["site"], TOKEN["name"], TOKEN["value"])

for table in SCHEMA["tables"]:
    with open(CONTENT_MANAGEMENT.format(table["query"]), "r") as f:
        query = f.read()

    data = ts.query_metadata(query)
    data_map = getattr(GraphQL, table["name"])(data)

    hc.populate_extract(table["name"], data_map)

print("complete")