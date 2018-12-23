from requests_oauthlib import OAuth2Session

from config.creds_store import get_access_token, save_access_token
from settings import STRAVA_CLIENT_ID, STRAVA_API_BASE_URL, REFRESH_TOKEN_URL, STRAVA_CLIENT_SECRET

token = get_access_token()
client = OAuth2Session(STRAVA_CLIENT_ID, token=token, auto_refresh_url=REFRESH_TOKEN_URL,
                       auto_refresh_kwargs=dict(client_id=STRAVA_CLIENT_ID, client_secret=STRAVA_CLIENT_SECRET),
                       token_updater=save_access_token)


def _url(path):
    return STRAVA_API_BASE_URL + path


def _json(response):
    response.raise_for_status()
    return response.json()


def get():
    response = client.get(_url('/athlete/activities'))
    return _json(response)
