import click

from decorators import format_result
from emoji import UP_ARROW, DOWN_ARROW, RIGHT_ARROW, RED_HEART, RUNNING_SHOE
from formatters import format_activity_type, format_distance, format_elevation, format_heartrate, format_speed, \
    humanize, format_date, format_seconds

N_A = 'N/A'

SUMMARY_ACTIVITY_FORMATTERS = {
    'start_date': format_date,
    'elapsed_time': format_seconds,
    'distance': format_distance,
    'average_speed': format_speed
}

SUMMARY_ACTIVITY_COLUMNS = [
    'index',
    'start_date',
    'name',
    'elapsed_time',
    'distance',
    'average_speed'
]


@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def format_activities_result(result, index_offset, output=None, quiet=None):
    return result if (quiet or output == 'json') else [
        _format_summary_activity(index + index_offset, activity) for
        index, activity in
        enumerate(result)]


@format_result(table_columns=['key', 'value'], show_table_headers=False, table_format='plain')
def format_activity_result(result, output):
    return result if output == 'json' else _format_activity(result)


def _format_activity_name(name, activity):
    activity_type = format_activity_type(activity.get('type'))
    is_race = activity.get('workout_type', 0) == 1
    return f'{activity_type} {click.style(name, bold=is_race)}'


def _format_summary_activity(index, activity):
    def format_name(name):
        return _format_activity_name(name, activity)

    formatters = {
        'name': format_name,
        **SUMMARY_ACTIVITY_FORMATTERS
    }

    return {
        'index': index,
        **_apply_formatters(activity, formatters)
    }


def _format_activity(activity):
    def format_name(name):
        return _format_activity_name(name, activity)

    def no_formatter(value):
        return value

    def format_gear(gear):
        return f'{gear.get("name")} ({format_distance(gear.get("distance", 0))})'

    def format_elevation_difference(elevation_difference):
        difference = round(elevation_difference)
        arrow = UP_ARROW if difference > 0 else DOWN_ARROW if difference < 0 else RIGHT_ARROW
        return f"{arrow} {format_elevation(elevation_difference)}"

    def format_split(split):
        average_heartrate = f"{click.style(RED_HEART, fg='red')} {format_heartrate(split['average_heartrate'])}" \
            if 'average_heartrate' in split else ''
        average_speed = f"{click.style(RUNNING_SHOE, fg='yellow')} {format_speed(split['average_speed'])}" \
            if 'average_speed' in split else ''
        elevation_difference = format_elevation_difference(split['elevation_difference']) \
            if 'elevation_difference' in split else ''
        return f'{average_speed} {average_heartrate} {elevation_difference}'

    def format_property(name):
        return click.style(f'{humanize(name)}:', bold=True)

    formatters = {
        'name': format_name,
        'description': no_formatter,
        **SUMMARY_ACTIVITY_FORMATTERS,
        'total_elevation_gain': format_elevation,
        'calories': no_formatter,
        'device_name': no_formatter,
        'gear': format_gear,
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
