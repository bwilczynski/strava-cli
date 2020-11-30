from ._helpers import client, url, json


def post_upload(xargs, filename):
    response=None
    #with open(filename, 'rb') as f:
    files={"file": open(filename, 'rb')}
    response = client.post(url=url(f'/uploads'), data=xargs, files=files)
    try:
        return json(response)
    except:
        return response

def get_upload(upload_id):
    response = client.get(url(f'/uploads/{upload_id}'))
    return json(response)
