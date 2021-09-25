from requests_oauthlib import OAuth2Session

from strava.config.creds_store import save_access_token, get_access_token
from strava.settings import (
    STRAVA_API_BASE_URL,
    STRAVA_CLIENT_ID,
    REFRESH_TOKEN_URL,
    STRAVA_CLIENT_SECRET,
)


def url(path):
    return STRAVA_API_BASE_URL + path


def json(response):
    response.raise_for_status()
    return response.json()


token = get_access_token()
client = OAuth2Session(
    STRAVA_CLIENT_ID,
    token=token,
    auto_refresh_url=REFRESH_TOKEN_URL,
    auto_refresh_kwargs=dict(
        client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET
    ),
    token_updater=save_access_token,
)
