from tableauserverclient.server.server import Server
from tableauserverclient.models.personal_access_token_auth import (
    PersonalAccessTokenAuth,
)


class Tableau:
    def __init__(self, server, site, token_name, token):
        self.auth = PersonalAccessTokenAuth(token_name, token, site)
        self.server = Server(server, True)

    def query_metadata(self, query):
        with self.server.auth.sign_in(self.auth):
            return self.server.metadata.query(query)["data"]
