from strava.config import local_store

CONFIG_FILE = "config.json"


def save_config(data):
    local_store.save(CONFIG_FILE, data)


def get_config():
    return local_store.load(CONFIG_FILE)


def delete_config():
    local_store.delete(CONFIG_FILE)
