from requests_oauthlib import OAuth2Session

from strava.settings import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, CLIENT_REDIRECT_URL, AUTH_URL, ACCESS_TOKEN_URL, \
    CLIENT_SCOPE

client = OAuth2Session(STRAVA_CLIENT_ID, redirect_uri=CLIENT_REDIRECT_URL, scope=CLIENT_SCOPE)


def login():
    return client.authorization_url(AUTH_URL)


def get_access_token(code):
    return client.fetch_token(ACCESS_TOKEN_URL, code=code, client_id=STRAVA_CLIENT_ID,
                              client_secret=STRAVA_CLIENT_SECRET)
