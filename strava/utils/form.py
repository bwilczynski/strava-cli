import itertools
import math
import shelve
from strava import api
from strava.utils.activity_common import add_metrics_to_activity

from strava.config.local_store import _get_fullpath


def compute_CTL(tss_table):
    #TODO is ewm capable of doing the same?
    CTL_yesterday = 0
    for index, row in tss_table.iterrows():
        alpha = math.exp(-1/42)
        CTL = row['tss'] * (1-alpha) + CTL_yesterday * alpha
        CTL_yesterday = CTL

    return round(CTL)


def compute_ATL(tss_table):
    #TODO is ewm capable of doing the same?
    ATL_yesterday = 0
    for index, row in tss_table.iterrows():
        alpha = math.exp(-1/7)
        ATL = row['tss'] * (1-alpha) + ATL_yesterday * alpha
        ATL_yesterday = ATL

    return round(ATL)


def get_tss_entry(act_id):
    activity = api.get_activity(act_id)
    tss_entry = add_metrics_to_activity(activity)[0].get('tss')
    date = activity.get('start_date')[0:10]
    return {date: tss_entry}


def compute_daily_tss(tss_entries):
    grouped_entries = [list(g) for _, g in itertools.groupby(tss_entries, lambda x: x.keys())]
    daily_tss = [{[k for k, v in g[0].items()][0]: sum([(v) for g1 in g for k, v in g1.items()])} for g in grouped_entries]

    dict_tss = {}
    for dt in daily_tss:
        dict_tss.update(dt)

    return dict_tss


def write_cache(key, value):
    cache = shelve.open(_get_fullpath('cache'))
    cache[key] = value
    cache.close()


def read_cache(key):
    cache = shelve.open(_get_fullpath('cache'))
    if key in cache:
        value = cache[key]
    cache.close()
    return value


def list_cache():
    cache = shelve.open(_get_fullpath('cache'))
    keys = list(cache.keys())
    cache.close()
    return keys


def delete_cache(key):
    cache = shelve.open(_get_fullpath('cache'))
    try:
        del cache[key]
    except KeyError:
        pass
    cache.close()


def clean_cache():
    cache = shelve.open(_get_fullpath('cache'))
    keys = list(cache.keys())
    for key in keys:
        del cache[key]
    cache.close()

