import webbrowser

import click

from strava.api import oauth2
from strava.config import creds_store
from strava.decorators import config_required
from strava.settings import (
    STRAVA_CLIENT_ID,
    STRAVA_CLIENT_SECRET,
    CLIENT_SCOPE,
    AUTH_URL,
    TOKEN_URL,
)


@click.command()
@config_required
def login():
    auth_flow = oauth2.OAuth2AuthorizationCodeFlow(
        client_id=STRAVA_CLIENT_ID,
        client_secret=STRAVA_CLIENT_SECRET,
        scope=CLIENT_SCOPE,
        auth_url=AUTH_URL,
        token_url=TOKEN_URL,
    )
    url, state = auth_flow.authorization_url()
    webbrowser.open_new(url)
    try:
        code = auth_flow.get_authorization_code(state)
        data = auth_flow.get_access_token(code)
        creds_store.save_access_token(data)
        click.echo("Login successful.")
    except oauth2.AuthenticationError:
        click.echo("Access was denied!")
        exit(1)
