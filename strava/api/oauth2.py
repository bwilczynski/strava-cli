import os
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

from requests_oauthlib import OAuth2Session


class AuthenticationError(Exception):
    pass


class OAuth2AuthorizationCodeFlow(object):
    def __init__(
        self,
        client_id=None,
        client_secret=None,
        scope=None,
        auth_url=None,
        token_url=None,
    ):
        class ClientRedirectServer(HTTPServer):
            query_params = {}

        class ClientRedirectHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query_string = self.path.split("?", 1)[-1]
                self.server.query_params = parse.parse_qs(query_string)

                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                html_file = os.path.join(
                    os.path.dirname(os.path.realpath(__file__)),
                    "templates",
                    "ok.html" if "code" in query_string else "fail.html",
                )
                with open(html_file, "rb") as html_view:
                    self.wfile.write(html_view.read())

            def log_message(self, format, *args):
                pass

        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.auth_url = auth_url
        self.token_url = token_url

        self.server = ClientRedirectServer(("", 0), ClientRedirectHandler)
        redirect_uri = f"http://localhost:{self.server.server_port}"
        self.client = OAuth2Session(
            self.client_id, redirect_uri=redirect_uri, scope=self.scope
        )

    def authorization_url(self):
        return self.client.authorization_url(self.auth_url)

    def get_authorization_code(self, state):
        while True:
            self.server.handle_request()
            if "code" in self.server.query_params:
                code_param = self.server.query_params["code"][0]
                state_param = (
                    self.server.query_params["state"][0]
                    if "state" in self.server.query_params
                    else None
                )

                if state == state_param:
                    return code_param
                else:
                    raise AuthenticationError()
            if "error" in self.server.query_params:
                raise AuthenticationError()

    def get_access_token(self, code):
        return self.client.fetch_token(
            self.token_url,
            code=code,
            client_id=self.client_id,
            client_secret=self.client_secret,
            include_client_id=True,
        )
