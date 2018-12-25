from ._api import url, json, client


def get_activities(page=None, per_page=None):
    response = client.get(url('/athlete/activities'), params=dict(page=page, per_page=per_page))
    return json(response)


def get_athlete():
    response = client.get(url('/athlete'))
    return json(response)


def get_stats(athlete_id):
    response = client.get(url(f'/athletes/{athlete_id}/stats'))
    return json(response)
