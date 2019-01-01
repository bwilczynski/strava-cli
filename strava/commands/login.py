import os
import webbrowser
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib import parse

import click

from strava import api
from strava.config import creds_store
from strava.decorators import config_required
from strava.settings import CLIENT_REDIRECT_PORT_NO


class AuthenticationError(Exception):
    pass


def _get_access_token(code):
    return api.get_access_token(code)


def _get_authorization_code(state):
    class ClientRedirectServer(HTTPServer):
        query_params = {}

    class ClientRedirectHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            query_string = self.path.split('?', 1)[-1]
            self.server.query_params = parse.parse_qs(query_string)

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            html_file = os.path.join(os.path.dirname(os.path.realpath(
                __file__)), 'templates', 'ok.html' if 'code' in query_string else 'fail.html')
            with open(html_file, 'rb') as html_view:
                self.wfile.write(html_view.read())

        def log_message(self, format, *args):
            pass

    server = ClientRedirectServer(('', CLIENT_REDIRECT_PORT_NO), ClientRedirectHandler)
    while True:
        server.handle_request()
        if 'code' in server.query_params:
            code_param = server.query_params['code'][0]
            state_param = server.query_params['state'][0] if 'state' in server.query_params else None

            if state == state_param:
                return code_param
            else:
                raise AuthenticationError()
        if 'error' in server.query_params:
            raise AuthenticationError()


@click.command()
@config_required
def login():
    url, state = api.login()
    webbrowser.open_new(url)
    try:
        code = _get_authorization_code(state)
        data = _get_access_token(code)
        creds_store.save_access_token(data)
        click.echo('Login successful.')
    except AuthenticationError:
        click.echo('Access was denied!')
        exit(1)
