import click
from strava.utils.streams_ride import ride_detail
from strava.utils.streams_workout import workout_detail
from strava.utils.streams_run import run_detail

from strava import api
from strava.decorators import format_result, TableFormat, OutputType
from strava.formatters import format_property, apply_formatters, noop_formatter, format_seconds, \
    format_gear, format_date, format_distance, format_heartrate, format_elevation, humanize, update_activity_name, \
    id_url_formatter

_ACTIVITY_TOTAL_INIT = {'number_of_activities': 0, 'total_time': 0, 'total_tss': 0}
_ACTIVITY_TOTAL_FORMATTERS = {
    'number_of_activities': noop_formatter,
    'total_time': format_seconds,
    'total_tss': noop_formatter,
}
_ACTIVITY_COLUMNS = ('key', 'value')
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


def get_activity_from_ids(output, activity_ids, details=False, total=False, from_=None, to=None, ftp=None):
    activity_total = _ACTIVITY_TOTAL_INIT
    for i, activity_id in enumerate(activity_ids):
        if i > 0:
            click.echo()

        # Gets the activity.
        activity = api.get_activity(activity_id)
        activity['name'] = update_activity_name(activity)

        # Add details if asked.
        met_formatters = None
        if details or total:
            act_type = activity.get('type')
            if act_type == 'Ride' or act_type == 'VirtualRide':
                metrics, met_formatters = ride_detail(activity, from_, to, ftp)
            elif act_type == 'Run':
                metrics, met_formatters = run_detail(activity, from_, to)
            elif act_type == 'Workout':
                metrics, met_formatters = workout_detail(activity, from_, to)
            else:
                metrics = {'tss': 0}
            # Returns the details.
            activity.update(metrics)

        _format_activity(activity, met_formatters, output=output)

        # Adapts totals.
        if total:
            activity_total['total_tss'] += activity.get('tss')
            activity_total['total_time'] += activity.get('moving_time')
            activity_total['number_of_activities'] += 1

    # Return the totals.
    if total:
        click.echo('\nTotal')
        _format_activity_total(activity_total, output=output)


@format_result(table_columns=_ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_activity(activity, formatters=None, output=None):
    final_formatters = [_ACTIVITY_TITLE_FORMATTERS, _ACTIVITY_DEFAULT_FORMATTERS]
    if formatters:
        final_formatters.append(formatters)
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


@format_result(table_columns=_ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_activity_total(activity, output=None):
    final_formatters = [_ACTIVITY_TOTAL_FORMATTERS]
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


def _as_table(activity, formatters):
    table = []
    for i in range(0, len(formatters)):
        table.extend([{'key': format_property(k), 'value': v}
                      for k, v in apply_formatters(activity, formatters[i]).items()])
        table.extend([{'key': '---', 'value': '---'}])
    return table
