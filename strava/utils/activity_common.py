import click

from strava.utils.streams_other import other_detail
from strava.utils.streams_ride import ride_detail
from strava.utils.streams_workout import workout_detail
from strava.utils.streams_run import run_detail

from strava import api
from strava.decorators import format_result, TableFormat, OutputType
from strava.formatters import format_property, apply_formatters, noop_formatter, format_seconds, \
    format_gear, format_date, format_distance, format_heartrate, format_elevation, update_activity_name, \
    id_url_formatter

ACTIVITY_TOTAL_INIT = {
    'bike #': 0,
    'run #': 0,
    'swim #': 0,
    'strength #': 0,
    'other #': 0,
    'total_time': 0,
    'total_tss': 0,
}
ACTIVITY_TOTAL_FORMATTERS = {
    'total_tss': noop_formatter,
    'total_time': format_seconds,
    'bike #': noop_formatter,
    'run #': noop_formatter,
    'swim #': noop_formatter,
    'strength #': noop_formatter,
    'other #': noop_formatter,
}
ACTIVITY_COLUMNS = ('key', 'value')
_ACTIVITY_TITLE_FORMATTERS = {
    'name': noop_formatter,
    'id': id_url_formatter,
}
_ACTIVITY_DEFAULT_FORMATTERS = {
    'gear': format_gear,
    'start_date': format_date,
    'moving_time': format_seconds,
    'distance': format_distance,
    'average_heartrate': format_heartrate,
    'total_elevation_gain': format_elevation,
}
_ACTIVITY_DEFAULT_LAP_FORMATTERS = {
    'lap_name': noop_formatter,
    'lap_time': format_seconds,
    'average_heartrate': format_heartrate,
    'max_heartrate': format_heartrate,
    'distance': format_distance,
    'total_elevation_gain': format_elevation,
}


def get_activity_from_ids(output, activity_ids, details=False, total=False, from_=None, to=None, ftp=None):
    activity_total = ACTIVITY_TOTAL_INIT.copy()
    for i, activity_id in enumerate(activity_ids):
        if i > 0:
            click.echo()

        # Gets the activity.
        activity = api.get_activity(activity_id)
        activity['name'] = update_activity_name(activity)

        # Add details if asked.
        met_formatters = None
        if details or total:
            activity, met_formatters, activity_total = add_metrics_to_activity(activity, activity_total, from_, to, ftp)

        if details:
            format_activity(activity, met_formatters, output=output)
        elif not total:
            format_activity(activity, None, output=output)

        # Adapts totals.
        if total:
            activity_total['total_tss'] += activity.get('tss')
            activity_total['total_time'] += activity.get('moving_time')

    # Return the totals.
    if total:
        click.echo('\nTotal')
        for (key, value) in activity_total.items():
            if value == 0:
                ACTIVITY_TOTAL_FORMATTERS.pop(key)
        _format_activity_total(activity_total, output=output)


def get_lap(output, activity, lap, ftp):
    # Get the sec boundary for the lap.
    laps = activity.get('laps')
    from_ = laps[lap].get('start_index')
    to = laps[lap].get('end_index')

    # Compute the metrics for that part.
    act, met_form, _ = add_metrics_to_activity(activity, activity_total=None, from_=from_, to=to, ftp=ftp)
    act['lap_name'] = activity.get('laps')[lap].get('name')
    act['lap_time'] = activity.get('laps')[lap].get('moving_time')
    act['average_heartrate'] = activity.get('laps')[lap].get('average_heartrate')
    act['max_heartrate'] = activity.get('laps')[lap].get('max_heartrate')
    act['distance'] = activity.get('laps')[lap].get('distance')
    act['total_elevation_gain'] = activity.get('laps')[lap].get('total_elevation_gain')

    return _format_activity_lap(act, met_form, output)


def add_metrics_to_activity(activity, activity_total=None, from_=None, to=None, ftp=None):
    met_formatters = None

    act_type = activity.get('type')
    if act_type == 'Ride' or act_type == 'VirtualRide':
        metrics, met_formatters = ride_detail(activity, from_, to, ftp)
        if activity_total:
            activity_total['bike #'] += 1
    elif act_type == 'Run':
        metrics, met_formatters = run_detail(activity, from_, to)
        if activity_total:
            activity_total['run #'] += 1
    elif act_type == 'Workout':
        metrics, met_formatters = workout_detail(activity, from_, to)
        if activity_total:
            activity_total['strength #'] += 1
    elif act_type == 'Swim':
        metrics = {'tss': 0}
        if activity_total:
            activity_total['swim #'] += 1
    else:
        metrics, met_formatters = other_detail(activity, from_, to)
        if activity_total:
            activity_total['other #'] += 1

    # Returns the details.
    activity.update(metrics)
    return activity, met_formatters, activity_total


@format_result(table_columns=ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def format_activity(activity, formatters=None, output=None):
    final_formatters = [_ACTIVITY_TITLE_FORMATTERS, _ACTIVITY_DEFAULT_FORMATTERS]
    if formatters:
        final_formatters.append(formatters)
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


@format_result(table_columns=ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_activity_total(activity, output=None):
    final_formatters = [ACTIVITY_TOTAL_FORMATTERS]
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


@format_result(table_columns=ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_activity_lap(activity, formatters=None, output=None):
    final_formatters = [_ACTIVITY_DEFAULT_LAP_FORMATTERS]
    if formatters:
        final_formatters.append(formatters)
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


def _as_table(activity, formatters):
    table = []
    for i in range(0, len(formatters)):
        table.extend([{'key': format_property(k), 'value': v}
                      for k, v in apply_formatters(activity, formatters[i]).items()])
        if i != len(formatters)-1:
            table.extend([{'key': '---', 'value': '---'}])
    return table
