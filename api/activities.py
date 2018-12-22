from requests_oauthlib import OAuth2Session

from config.creds_store import get_access_token
from decorators import auto_refresh_token
from settings import STRAVA_CLIENT_ID, STRAVA_API_BASE_URL

token = get_access_token()
client = OAuth2Session(STRAVA_CLIENT_ID, token=token)


def _url(path):
    return STRAVA_API_BASE_URL + path


def _json(response):
    response.raise_for_status()
    return response.json()


@auto_refresh_token(client)
def get():
    response = client.get(_url('/athlete/activities'))
    return _json(response)
