from hypergraph.graphql import flatten_results
from hypergraph.hyper import HyperCreator
from hypergraph.tableau import Tableau
import yaml

CONTENT_MANAGEMENT = "./resources/content_management/{}"
SCHEMA_FILE = "./resources/content_management/schema.yaml"
HYPER_FILE = "./build/tableau.hyper"
TOKEN_FILE = "./resources/token"

with open(SCHEMA_FILE, "r") as f:
    SCHEMA = yaml.safe_load(f)

with open(TOKEN_FILE, "r") as f:
    TOKEN = yaml.safe_load(f)

hc = HyperCreator(SCHEMA, HYPER_FILE)
ts = Tableau(TOKEN["server"], TOKEN["site"], TOKEN["name"], TOKEN["value"])

for table in SCHEMA["tables"]:
    if table["name"] != "content":
        break

    with open(CONTENT_MANAGEMENT.format(table["query"]), "r") as f:
        query = f.read()

    data = ts.query_metadata(query)
    data = flatten_results(data)

    hc.populate_extract(table["name"], data)

print(hc.tables)