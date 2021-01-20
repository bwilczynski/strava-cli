from ._helpers import client, url, json


def get_streams(activity_id, key):
    response = client.get(url(f'/activities/{activity_id}/streams'), params={'keys': [key]})
    return json(response)
