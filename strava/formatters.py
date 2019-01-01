import math
import re
from datetime import datetime, timezone

import click

from strava import emoji

N_A = 'N/A'


def format_seconds(seconds):
    if seconds > 3600:
        mins = math.floor(seconds / 60)
        return f'{math.floor(mins / 60):.0f}h {mins % 60:.0f}m'
    else:
        return f'{math.floor(seconds / 60):02.0f}:{seconds % 60:02.0f}'


def format_date(date):
    utc_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return utc_date.replace(tzinfo=timezone.utc).astimezone()


def format_distance(distance):
    distance_km = math.floor(distance / 10) / 100
    return f'{distance_km:.2f} km'


def format_speed(speed):
    return f'{format_seconds(1000 / speed)} /km' if speed > 0 else None


def format_heartrate(heartrate):
    return f'{heartrate:.0f} bpm'


def format_activity_type(activity_type):
    type_emojis = {
        'run': emoji.PERSON_RUNNING,
        'ride': emoji.PERSON_BIKING,
        'swim': emoji.PERSON_SWIMMING,
        'workout': emoji.PERSON_LIFTING_WEIGHTS
    }
    return type_emojis.get(activity_type.lower(), '')


def format_elevation(elevation):
    return f'{round(elevation)} m'


def humanize(word):
    word = word.replace('_', ' ')
    word = re.sub(r"(?i)([a-z\d]*)", lambda m: m.group(1).lower(), word)
    word = re.sub(r"^\w", lambda m: m.group(0).upper(), word)
    return word


def noop_formatter(value):
    return value


def format_activity_name(name, activity):
    activity_type = format_activity_type(activity.get('type'))
    is_race = activity.get('workout_type', 0) == 1
    return f'{activity_type} {click.style(name, bold=is_race)}'


def apply_formatters(activity, formatters):
    return {k: formatter(activity[k]) if k in activity else N_A for k, formatter in formatters.items()}
