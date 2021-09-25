from ._helpers import client, url, json


def get_activity(activity_id):
    response = client.get(url(f"/activities/{activity_id}"))
    return json(response)
