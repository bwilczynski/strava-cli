from functools import reduce

import click
import pandas as pd

from strava import api
from strava.formatters import noop_formatter
from strava.utils import to_dataframe, filter_stream_by_from_to, compute_hrtss


def other_detail(activity, from_, to):
    sensors = ['time', 'heartrate']

    # Gets the streams needed.
    stream_by_keys = [to_dataframe(api.get_streams(activity.get('id'), key=key)) for key in sensors]

    # Check the sensors available.
    sensors_available = [list(sbk.columns) for sbk in stream_by_keys]
    flat_sensors_available = [item for sublist in sensors_available for item in sublist]
    if all([s in flat_sensors_available for s in sensors]):
        # Try to merge the streams.
        try:
            stream = reduce(lambda left, right: pd.merge(left, right, on='distance'), stream_by_keys)
        except KeyError:
            try:
                stream = reduce(lambda left, right: pd.merge(left, right, on='time'), stream_by_keys)
            except KeyError:
                click.echo('Enable to merge the streams on distance or time.')

        stream = stream.drop_duplicates(subset='time')
        stream = filter_stream_by_from_to(stream, from_, to)

        # Could had more cases here:
        metrics, formatters = _other_detail(stream)
        return metrics, formatters
    else:
        return {'tss': 0}, {'tss': noop_formatter}


def _other_detail(stream):
    # Computes metrics.
    metrics = dict({
        'tss': compute_hrtss(stream),
    })
    formatters = {
        'tss': noop_formatter,
    }
    return metrics, formatters
