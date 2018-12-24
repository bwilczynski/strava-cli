from datetime import datetime, timezone
from math import floor

import click


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


def format_actvity_type(activity_type):
    type_emojis = {
        'run': u'\U0001F3C3',
        'ride': u'\U0001F6B4',
        'swim': u'\U0001F3CA',
        'workout': u'\U0001F3CB'
    }
    return type_emojis.get(activity_type.lower(), '')


def format_elevation(elevation):
    return f'{elevation:.0f} m'


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


def format_athlete(athlete):
    def format_name():
        return f'{athlete.get("firstname")} {athlete.get("lastname")}'

    return [
        {'key': 'id', 'value': athlete.get('id')},
        {'key': 'username', 'value': athlete.get('username')},
        {'key': 'name', 'value': format_name()},
        {'key': 'email', 'value': athlete.get('email')}
    ]


def format_recent_stats(stats):
    return _format_stats(stats, lambda activity_type: f'recent_{activity_type}_totals')


def format_ytd_stats(stats):
    return _format_stats(stats, lambda activity_type: f'ytd_{activity_type}_totals')


def _format_stats(stats, get_property_func):
    formatters = {
        'count': lambda x: x,
        'distance': format_distance,
        'moving_time': format_seconds,
        'elevation_gain': format_elevation
    }

    def format_totals(totals):
        return {k: formatter(totals.get(k)) for k, formatter in formatters.items()}

    return [
        dict(format_totals(stats[f'{get_property_func(activity_type)}']),
             **dict(type=format_actvity_type(f'{activity_type}')))
        for activity_type in ['run', 'ride', 'swim']
    ]
