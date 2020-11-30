from ._helpers import client, url, json


def post_upload(xargs):
    response = client.post(url(f'/uploads'), data=xargs)
    return json(response)
