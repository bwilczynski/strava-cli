from ._helpers import url, json, client


def get_activities(**kwargs):
    response = client.get(url("/athlete/activities"), params=kwargs)
    return json(response)


def get_athlete():
    response = client.get(url("/athlete"))
    return json(response)


def get_stats(athlete_id):
    response = client.get(url(f"/athletes/{athlete_id}/stats"))
    return json(response)
