import click

from strava import api
from strava.decorators import format_result, TableFormat, OutputType
from strava.formatters import format_property, apply_formatters, noop_formatter, format_seconds, \
    format_gear, format_date, format_distance, format_heartrate, format_elevation, humanize

ACTIVITY_TOTAL_INIT = {'number_of_activities': 0, 'total_time': 0, 'total_tss': 0}
_ACTIVITY_TOTAL_FORMATTERS = {
    'number_of_activities': noop_formatter,
    'total_time': format_seconds,
    'total_tss': noop_formatter,
}
_ACTIVITY_COLUMNS = ('key', 'value')
_ACTIVITY_TITLE_FORMATTERS = {
    'name': humanize,
}
_ACTIVITY_DEFAULT_FORMATTERS = {
    'gear': format_gear,
    'start_date': format_date,
    'moving_time': format_seconds,
    'distance': format_distance,
    'average_heartrate': format_heartrate,
    'total_elevation_gain': format_elevation,
}


def get_athlete_ftp():
    try:
        ftp = api.get_athlete().get('ftp')
        assert isinstance(ftp, int)
        return ftp
    except:
        click.echo(f'The FTP has to be defined in your strava profile.')
        raise


@format_result(table_columns=_ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def format_activity(activity, formatters=None, output=None):
    final_formatters = [_ACTIVITY_TITLE_FORMATTERS, _ACTIVITY_DEFAULT_FORMATTERS]
    if formatters:
        final_formatters.append(formatters)
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


@format_result(table_columns=_ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def format_activity_total(activity, output=None):
    final_formatters = [_ACTIVITY_TOTAL_FORMATTERS]
    return activity if output == OutputType.JSON.value else _as_table(activity, final_formatters)


def _as_table(activity, formatters):
    table = []
    for i in range(0, len(formatters)):
        table.extend([{'key': format_property(k), 'value': v}
                      for k, v in apply_formatters(activity, formatters[i]).items()])
        table.extend([{'key': '---', 'value': '---'}])
    return table
