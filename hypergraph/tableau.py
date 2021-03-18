import tableauserverclient
from tableauserverclient.server.server import Server
from tableauserverclient.models.personal_access_token_auth import PersonalAccessTokenAuth

class Tableau(Server):
    def __init__(self, *args, **kwargs):
        self._auth = PersonalAccessTokenAuth(kwargs["token_name"], kwargs["token_value"])
        self._server = Server(kwargs["tableau_server"], True)
        