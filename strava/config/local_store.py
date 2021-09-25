import json
import os


def _get_local_store_dir():
    return os.path.expanduser(os.path.join("~", ".strava-cli"))


def _get_fullpath(filename):
    return os.path.join(_get_local_store_dir(), filename)


def save(filename, data):
    fullpath = _get_fullpath(filename)
    os.makedirs(os.path.dirname(fullpath), exist_ok=True)
    with os.fdopen(
        os.open(fullpath, os.O_RDWR | os.O_CREAT | os.O_TRUNC, 0o600), "w+"
    ) as file:
        json.dump(data, file)


def load(filename):
    fullpath = _get_fullpath(filename)
    if os.path.isfile(fullpath):
        with open(fullpath, "rb") as file:
            return json.load(file)
    else:
        return None


def delete(filename):
    fullpath = _get_fullpath(filename)
    if os.path.isfile(fullpath):
        os.remove(fullpath)
