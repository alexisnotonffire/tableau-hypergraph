from tableauserverclient.server.server import Server
from tableauserverclient.models.personal_access_token_auth import (
    PersonalAccessTokenAuth,
)


class Tableau:
    """Provides convenience functions for interacting with Tableau APIs"""
    def __init__(self, server, site, token_name, token):
        """Initialises Tableau
        
        Args:
            server: URL of target Tableau server
            site: Tableau target site
            token_name: Name of the Personal Access Token used to authenticate
            token: Secret of the Personal Access Token used to authenticate
        """
        self.auth = PersonalAccessTokenAuth(token_name, token, site)
        self.server = Server(server, True)

    def query_metadata(self, query):
        """Runs query against the Metadata API

        Args:
            query: GraphQL query to be run against the metadata API

        Returns:
            Takes the "data" attribute of the API response JSON and returns as Dict.
        """
        with self.server.auth.sign_in(self.auth):
            return self.server.metadata.query(query)["data"]
