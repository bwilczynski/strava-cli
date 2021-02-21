import datetime
from math import floor, pow

import click
from numpy import mean

import pandas as pd

from strava import api


def to_dataframe(streams):
    data = [streams[i]['data'] for i in range(0, len(streams))]
    data_type = [streams[i]['type'] for i in range(0, len(streams))]
    return pd.DataFrame(list(zip(*data)), columns=data_type)


def filter_stream_by_from_to(stream, from_, to):
    # Apply the from-to if requested.
    time_range_secs = dict()
    if from_:
        time_range_secs['from'] = from_
    else:
        time_range_secs['from'] = min(stream['time'])
    if to:
        time_range_secs['to'] = to
    else:
        time_range_secs['to'] = max(stream['time'])
    filtered_stream = stream[[all(t) for t in zip(stream['time'] >= time_range_secs.get('from'),
                                                  stream['time'] <= time_range_secs.get('to'))]]
    return filtered_stream


def average(values):
    return floor(mean(values))


def normalized_power(time, power):
    """
    The normalized power is defined as follow:
    Step 1: Calculate the rolling average with a window of 30 seconds: Start at 30 seconds, calculate the average power of the previous 30 seconds and to the for every second after that.
    Step 2: Calculate the 4th power of the values from the previous step.
    Step 3: Calculate the average of the values from the previous step.
    Step 4: Take the fourth root of the average from the previous step. This is your normalized power.
    """
    power = pd.DataFrame(power.copy())
    indexed_power = power.set_index(pd.Series([datetime.datetime.fromtimestamp(t) for t in time]))
    rolling_power = indexed_power.rolling(window=datetime.timedelta(seconds=30)).mean()
    rolling_power = rolling_power.dropna()
    mean_power = mean([pow(p, 4) for p in rolling_power['watts']])
    return floor(pow(mean_power, 1/4))


def intensity_factor(n_power, ftp):
    """
    Compute the intensity factor with the following:
    IF = Intensity Factor
    NP = Normalized Power
    FTP = Functional Threshold Power

    by doing: IF = NP / FTP
    """
    return round(n_power / ftp, 2)


def training_stress_score(time, n_power, i_factor, ftp):
    """
    Compute the Training Stress Score with the following:
    Where the following is needed:
    TSS = Training Stress Score
    t = duration of workout in seconds
    NP = Normalized Power
    IF = Intensity Factor
    FTP = Functional Threshold Power

    by doing: ((t * NP * IF) / (FTP * 3600)) * 100
    """
    return floor((((time.iloc[-1]-time.iloc[0]) * n_power * i_factor) / (ftp * 3600)) * 100)


def efficiency_factor(stream):
    """
    The efficiency factor is computed with the following:
    EF = NP / average HR (for ride done is HR zone 2)
    The second heartrate zone is used from strava
    """
    try:
        zone_2_stream = _filter_stream_by_zone(stream, 2)
        if len(zone_2_stream) > 0:
            np = normalized_power(zone_2_stream['time'], zone_2_stream['watts'])
            average_heartrate = mean(zone_2_stream['heartrate'])
            return round(np / average_heartrate, 2)
    except:
        pass
    return ''


def variability_index(n_power, avg_power):
    """
    The ratio of NP to average power for a ride. Closely associated with pacing (Criterium can be high >1.3, CLM should be low <1.05).
    The variability index is computed as follow:
    VI = NP / average Power
    """
    return round(n_power / avg_power, 2)


def compute_hrtss(stream):
    """
    Accordingy to https://www.trainingpeaks.com/blog/estimating-training-stress-score-tss/
    the hrTSS is a way to compute the training stress score based on heart rate.

    The lowest number of zone 5 is the 100% FTHR (according to Joe Friel)
    """
    hrtss_table = {'1_low': 20, '1_medium': 30, '1_high': 40, '2_low': 50, '2_high': 60, '3': 70, '4': 80, '5a': 100, '5b': 120, '5c': 140}

    # Define the zones
    try:
        athlete_zones = api.get_zones().get('heart_rate').get('zones')
        assert len(athlete_zones) == 5
        fthr = athlete_zones[4].get('min')
        zones = _compute_hr_zones(fthr)
    except:
        click.echo('5 zones are not set in your strava account, please do that to compute the hrtss.')

    # Assign each entry to a zone.
    rep = pd.DataFrame()
    rep['time'] = stream['time'].diff()
    rep['heartrate'] = [_heartrate_to_zones(hr, zones) for hr in stream['heartrate']]
    rep = rep.dropna()

    hours_in_zones = rep.groupby('heartrate').sum()/3600
    hrtss = sum([hrtss_table[i] * r['time'] for i, r in hours_in_zones.iterrows()])
    return floor(hrtss)


def _compute_hr_zones(fthr):
    zones = {
        '1_low': {'min': 0, 'max': round(0.40 * fthr)},
        '1_medium': {'min': round(0.60 * fthr)+1, 'max': round(0.70 * fthr)},
        '1_high': {'min': round(0.70 * fthr)+1, 'max': round(0.81 * fthr)},
        '2_low': {'min': round(0.81 * fthr)+1, 'max': round(0.85 * fthr)},
        '2_high': {'min': round(0.85 * fthr)+1, 'max': round(0.89 * fthr)},
        '3': {'min': round(0.89 * fthr)+1, 'max': round(0.93 * fthr)},
        '4': {'min': round(0.93 * fthr)+1, 'max': round(0.99 * fthr)},
        '5a': {'min': round(0.99 * fthr)+1, 'max': round(1.02 * fthr)},
        '5b': {'min': round(1.02 * fthr)+1, 'max': round(1.06 * fthr)},
        '5c': {'min': round(1.06 * fthr)+1, 'max': 1000},
    }
    return zones


def _extract_zone(zones, zone_number):
    """ Return the min/max of the zone received."""
    zone = zones.get('heart_rate').get('zones')[zone_number-1]
    return zone.get('min'), zone.get('max')


def _heartrate_to_zones(heartrate, zones):
    for i in range(0, len(zones)):
        index = list(zones.keys())[i]
        if heartrate <= zones[index]['max']:
            return index


def _filter_stream_by_zone(stream, zone_number):
    zones = api.get_zones()
    zone_min, zone_max = _extract_zone(zones, zone_number)
    filtered_stream = stream[[all(t) for t in zip(stream['heartrate'] >= zone_min,
                                                  stream['heartrate'] <= zone_max)]]
    return filtered_stream

