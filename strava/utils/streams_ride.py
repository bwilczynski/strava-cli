import click
import pandas as pd

from functools import reduce

from strava import api
from strava.formatters import noop_formatter, format_power, format_cadence
from strava.utils import to_dataframe, filter_stream_by_from_to
from strava.utils.streams_computations import average, compute_hrtss
from strava.utils.streams_computations import normalized_power, intensity_factor, training_stress_score, variability_index, efficiency_factor


def ride_detail(activity, from_, to):
    if activity.get('device_watts'):
        sensors = ['time', 'watts', 'cadence', 'heartrate']
    else:
        sensors = ['time', 'cadence', 'heartrate']

    # Gets the streams needed.
    stream_by_keys = [to_dataframe(api.get_streams(activity.get('id'), key=key)) for key in sensors]
    stream = reduce(lambda left, right: pd.merge(left, right, on='distance'), stream_by_keys)
    stream = stream.drop_duplicates(subset='time')
    stream = filter_stream_by_from_to(stream, from_, to)

    if activity.get('device_watts'):
        metrics, formatters = _ride_detail_with_power(stream)
    else:
        metrics, formatters = _ride_detail_without_power(stream)
    return metrics, formatters


def get_athlete_ftp():
    try:
        ftp = api.get_athlete().get('ftp')
        assert isinstance(ftp, int)
        return ftp
    except:
        click.echo(f'The FTP has to be defined in your strava profile.')
        raise


def _ride_detail_without_power(stream):
    # Computes metrics.
    metrics = dict({
        'tss': compute_hrtss(stream),
        'average_cadence': average(stream['cadence'][stream['cadence'] != 0]),
    })
    formatters = {
        'tss': noop_formatter,
        'average_cadence': format_cadence,
    }
    return metrics, formatters


def _ride_detail_with_power(stream):
    # Gets the FTP.
    ftp = get_athlete_ftp()

    # Precomputes metrics.
    np = normalized_power(stream['time'], stream['watts'])
    avg_p = average(stream['watts'])
    if_ = intensity_factor(np, ftp)

    # Merge them into a single dict
    metrics = dict({
        'ftp': ftp,
        'normalized_power': np,
        'average_power': avg_p,
        'intensity_factor': if_,
        'tss': training_stress_score(stream['time'], np, if_, ftp),
        'variability_index': variability_index(np, avg_p),
        'efficiency_factor': efficiency_factor(stream),
        'average_cadence': average(stream['cadence'][stream['cadence'] != 0]),
    })

    # Define formatters
    formatters = {
        'tss': noop_formatter,
        'average_power': format_power,
        'normalized_power': format_power,
        'intensity_factor': noop_formatter,
        'variability_index': noop_formatter,
        'efficiency_factor': noop_formatter,
        'average_cadence': format_cadence,
        'ftp': format_power,
    }
    return metrics, formatters
