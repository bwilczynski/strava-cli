import os

from strava.config import config_store

cfg = config_store.get_config() or {}

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID") or cfg.get("client_id")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET") or cfg.get("client_secret")

STRAVA_AUTH_API_BASE_URL = "https://www.strava.com/oauth"
STRAVA_API_BASE_URL = "https://www.strava.com/api/v3"

CLIENT_SCOPE = ["activity:read_all,activity:write"]
AUTH_URL = f"{STRAVA_AUTH_API_BASE_URL}/authorize"
TOKEN_URL = f"{STRAVA_AUTH_API_BASE_URL}/token"
REFRESH_TOKEN_URL = TOKEN_URL

IMPERIAL_UNITS = False
