from datetime import datetime, timezone
from math import floor

from emoji import PERSON_RUNNING, PERSON_BIKING, PERSON_SWIMMING, PERSON_LIFTING_WEIGHTS


def format_seconds(seconds):
    if seconds > 3600:
        mins = floor(seconds / 60)
        return f'{floor(mins / 60):.0f}h {mins % 60:.0f}m'
    else:
        return f'{floor(seconds / 60):02.0f}:{seconds % 60:02.0f}'


def format_date(date):
    utc_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return utc_date.replace(tzinfo=timezone.utc).astimezone()


def format_distance(distance):
    distance_km = floor(distance / 10) / 100
    return f'{distance_km:.2f} km'


def format_speed(speed):
    return f'{format_seconds(1000 / speed)} /km' if speed > 0 else None


def format_heartrate(heartrate):
    return f'{heartrate:.0f} bpm'


def format_activity_type(activity_type):
    type_emojis = {
        'run': PERSON_RUNNING,
        'ride': PERSON_BIKING,
        'swim': PERSON_SWIMMING,
        'workout': PERSON_LIFTING_WEIGHTS
    }
    return type_emojis.get(activity_type.lower(), '')


def format_elevation(elevation):
    return f'{round(elevation)} m'
