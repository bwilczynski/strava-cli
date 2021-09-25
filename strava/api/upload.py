from requests import HTTPError

from ._helpers import client, url, json


def post_upload(xargs, filename):
    files = {"file": open(filename, "rb")}
    response = client.post(url=url("/uploads"), data=xargs, files=files)
    try:
        return json(response)
    except HTTPError:
        return response


def get_upload(upload_id):
    response = client.get(url(f"/uploads/{upload_id}"))
    return json(response)
