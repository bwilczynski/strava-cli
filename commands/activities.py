import click

import api.activity
from api import athlete
from decorators import login_required, format_result, output_option
from formatters import format_activity_type, format_date, format_distance, format_seconds, format_speed, \
    format_heartrate, format_elevation

SUMMARY_ACTIVITY_FORMATTERS = {
    'start_date': format_date,
    'distance': format_distance,
    'elapsed_time': format_seconds,
    'average_speed': format_speed,
    'max_speed': format_speed,
    'average_heartrate': format_heartrate,
    'max_heartrate': format_heartrate
}

SUMMARY_ACTIVITY_COLUMNS = ['start_date', 'name', 'distance', 'elapsed_time', 'average_speed', 'max_speed',
                            'average_heartrate',
                            'max_heartrate']


@click.command('activities')
@click.option('--page', '-P', default=1, type=int)
@click.option('--per_page', '-PP', default=30, type=int)
@output_option()
@login_required
@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def get_activities(output, page, per_page):
    result = athlete.get_activities(page, per_page)
    return result if output == 'json' else [_format_summary_activity(activity) for activity in result]


@click.command('activity')
@click.option('--index', '-I', default=1, type=int)
@output_option()
@login_required
@format_result(table_columns=['key', 'value'])
def get_activity(index, output):
    activities = athlete.get_activities(index, 1)
    activity = activities[-1]
    activity_id = activity.get('id')
    result = api.activity.get_activity(activity_id)
    return result if output == 'json' else _format_activity(result)


def _format_activity_name(name, activity):
    activity_type = format_activity_type(activity.get('type'))
    is_race = activity.get('workout_type', 0) == 1
    return f'{activity_type} {click.style(name, bold=is_race)}'


def _format_summary_activity(activity):
    def format_name(name):
        return _format_activity_name(name, activity)

    formatters = {
        'name': format_name,
        **SUMMARY_ACTIVITY_FORMATTERS
    }

    return _apply_formatters(activity, formatters)


def _format_activity(activity):
    def format_name(name):
        return _format_activity_name(name, activity)

    def no_formatter(value):
        return value

    def format_gear(gear):
        return f'{gear.get("name")} ({format_distance(gear.get("distance", 0))})'

    formatters = {
        'name': format_name,
        **SUMMARY_ACTIVITY_FORMATTERS,
        'total_elevation_gain': format_elevation,
        'calories': no_formatter,
        'device_name': no_formatter,
        'gear': format_gear,
    }
    activity = _apply_formatters(activity, formatters)

    return [
        {'key': k, 'value': v} for k, v in activity.items()
    ]


def _apply_formatters(activity, formatters):
    return {k: formatter(activity[k]) if k in activity else None for k, formatter in formatters.items()}
