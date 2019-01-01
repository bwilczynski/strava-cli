import os

from strava.config import config_store

cfg = config_store.get_config() or {}

STRAVA_CLIENT_ID = os.getenv('STRAVA_CLIENT_ID') or cfg.get('client_id')
STRAVA_CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET') or cfg.get('client_secret')

STRAVA_AUTH_API_BASE_URL = 'https://www.strava.com/oauth'
STRAVA_API_BASE_URL = 'https://www.strava.com/api/v3'

CLIENT_REDIRECT_PORT_NO = 5000
CLIENT_REDIRECT_URL = f'http://localhost:{CLIENT_REDIRECT_PORT_NO}'
CLIENT_SCOPE = ['activity:read_all']
AUTH_URL = f'{STRAVA_AUTH_API_BASE_URL}/authorize'
ACCESS_TOKEN_URL = f'{STRAVA_AUTH_API_BASE_URL}/token'
REFRESH_TOKEN_URL = ACCESS_TOKEN_URL
