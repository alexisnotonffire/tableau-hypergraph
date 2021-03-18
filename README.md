# Hypergraph
Tableau does not have a native GraphQL connector. This application provides a way to generate a Hyper extract from a GraphQL API and publish to a Tableau server.

# Usage
Hypergraph requires you provide:
* GraphQL endpoint and authentication
* GraphQL query for the endpoint
* Tableau server address and authentication
* Target datasource

Roughly speaking the following will then happen:
1. Hypergraph will authenticate against the GraphQL endpoint and collect the query response
1. A Hyper schema will be generated based on the query results
1. The query response will be flattened into the Hyper extract
1. The Hyper extract will then be published to the server
