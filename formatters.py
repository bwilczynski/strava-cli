from datetime import datetime, timezone
from math import floor

import click


def format_seconds(seconds):
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


def format_actvity_type(type):
    type_emojis = {
        'run': u'\U0001F3C3',
        'ride': u'\U0001F6B4',
        'swimming': u'\U0001F3CA',
        'workout': u'\U0001F3CB'
    }
    return type_emojis.get(type.lower(), '')


def format_activity(activity):
    def format_name(name):
        activity_type = format_actvity_type(activity['type'])
        is_race = 'workout_type' in activity and activity['workout_type'] == 1
        return f'{activity_type} {click.style(name, bold=is_race)}'

    formatters = {
        'name': format_name,
        'start_date': format_date,
        'distance': format_distance,
        'elapsed_time': format_seconds,
        'average_speed': format_speed,
        'max_speed': format_speed,
        'average_heartrate': format_heartrate,
        'max_heartrate': format_heartrate
    }

    return {k: formatter(activity[k]) if k in activity else None for k, formatter in formatters.items()}
