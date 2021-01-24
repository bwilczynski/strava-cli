from functools import reduce

import pandas as pd

from strava import api
from strava.formatters import noop_formatter
from strava.utils import to_dataframe, filter_stream_by_from_to, compute_hrtss


def workout_detail(activity, from_, to):
    sensors = ['time', 'heartrate']

    # Gets the streams needed.
    stream_by_keys = [to_dataframe(api.get_streams(activity.get('id'), key=key)) for key in sensors]
    stream = reduce(lambda left, right: pd.merge(left, right, on='time'), stream_by_keys)
    stream = stream.drop_duplicates(subset='time')
    stream = filter_stream_by_from_to(stream, from_, to)

    # Could had more cases here:
    metrics, formatters = _workout_detail(stream)
    return metrics, formatters


def _workout_detail(stream):
    # Computes metrics.
    metrics = dict({
        'tss': compute_hrtss(stream),
    })
    formatters = {
        'tss': noop_formatter,
    }
    return metrics, formatters
