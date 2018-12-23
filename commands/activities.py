from datetime import datetime, timezone
from math import floor

import click

from api import activities
from decorators import login_required, format_result, output_option


@click.command('activities')
@output_option()
@login_required
@format_result(
    headers=['start_date', 'name', 'distance', 'elapsed_time', 'average_speed', 'max_speed', 'average_heartrate', 'max_heartrate'])
def get_activities():
    result = activities.get()
    return result, [_format_activity(activity) for activity in result]


def _format_activity(activity):
    def format_seconds(seconds):
        return f'{floor(seconds / 60):02.0f}:{seconds % 60:02.0f}'

    def format_date(date):
        utc_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        return utc_date.replace(tzinfo=timezone.utc).astimezone()

    def format_distance(distance):
        distance_km = floor(distance / 10) / 100
        return f'{distance_km:.2f} km'

    def format_speed(speed):
        return f'{format_seconds(1000 / speed)} /km'

    def format_heartrate(heartrate):
        return f'{heartrate:.0f} bpm'

    formatters = {
        'name': lambda x: click.style(x, bold=True),
        'start_date': format_date,
        'distance': format_distance,
        'elapsed_time': format_seconds,
        'average_speed': format_speed,
        'max_speed': format_speed,
        'average_heartrate': format_heartrate,
        'max_heartrate': format_heartrate
    }

    return {k: formatter(activity[k]) for k, formatter in formatters.items()}
