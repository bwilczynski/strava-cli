from strava.config import local_store

ACCESS_TOKEN_FILE = "access_token.json"


def save_access_token(data):
    local_store.save(ACCESS_TOKEN_FILE, data)


def get_access_token():
    return local_store.load(ACCESS_TOKEN_FILE)


def delete_access_token():
    local_store.delete(ACCESS_TOKEN_FILE)
