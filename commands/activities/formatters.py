import click

from decorators import format_result, OutputType, TableFormat
from emoji import UP_ARROW, DOWN_ARROW, RIGHT_ARROW, RED_HEART, RUNNING_SHOE
from formatters import format_activity_type, format_distance, format_elevation, format_heartrate, format_speed, \
    humanize, format_date, format_seconds, noop_formatter

N_A = 'N/A'

SUMMARY_ACTIVITY_FORMATTERS = {
    'id': noop_formatter,
    'start_date': format_date,
    'elapsed_time': format_seconds,
    'distance': format_distance,
    'average_speed': format_speed
}

SUMMARY_ACTIVITY_COLUMNS = [
    'id',
    'start_date',
    'name',
    'elapsed_time',
    'distance',
    'average_speed'
]

ACTIVITY_COLUMNS = ['key', 'value']


@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def format_activities(result, output=None, quiet=None):
    return result if (quiet or output == OutputType.JSON.value) else [
        _format_summary_activity(activity) for
        activity in result]


@format_result(table_columns=ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def format_activity(result, output):
    return result if output == OutputType.JSON.value else _format_activity(result)


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

    def format_gear(gear):
        return f'{gear.get("name")} ({format_distance(gear.get("distance", 0))})'

    def format_heartrate_with_emoji(heartrate):
        return f"{click.style(RED_HEART, fg='red')} {format_heartrate(heartrate)}"

    def format_speed_with_emoji(speed):
        return f"{click.style(RUNNING_SHOE, fg='yellow')} {format_speed(speed)}"

    def format_elevation_with_emoji(elevation):
        difference = round(elevation)
        arrow = UP_ARROW if difference > 0 else DOWN_ARROW if difference < 0 else RIGHT_ARROW
        return f"{arrow} {format_elevation(abs(elevation))}"

    def format_split(split):
        average_heartrate = format_heartrate_with_emoji(split['average_heartrate']) \
            if 'average_heartrate' in split else ''
        average_speed = format_speed_with_emoji(split['average_speed']) \
            if 'average_speed' in split else ''
        elevation_difference = format_elevation_with_emoji(split['elevation_difference']) \
            if 'elevation_difference' in split else ''
        return f'{average_speed} {average_heartrate} {elevation_difference}'

    def format_property(name):
        return click.style(f'{humanize(name)}:', bold=True)

    formatters = {
        'name': format_name,
        'description': noop_formatter,
        **SUMMARY_ACTIVITY_FORMATTERS,
        'max_speed': format_speed,
        'average_heartrate': format_heartrate,
        'max_heartrate': format_heartrate,
        'total_elevation_gain': format_elevation,
        'calories': noop_formatter,
        'device_name': noop_formatter,
        'gear': format_gear
    }

    basic_data = [
        {'key': format_property(k), 'value': v} for k, v in _apply_formatters(activity, formatters).items()
    ]
    split_data = [
        {'key': format_property(f"Split {split.get('split')}"), 'value': format_split(split)} for split in
        activity.get('splits_metric')
    ]

    return [
        *basic_data,
        *split_data
    ]


def _apply_formatters(activity, formatters):
    return {k: formatter(activity[k]) if k in activity else N_A for k, formatter in formatters.items()}
