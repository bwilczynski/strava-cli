import click
import datetime
from itertools import compress

from strava import api
from strava.decorators import output_option, login_required, TableFormat, format_result, OutputType
from strava.commands.activities_weekly import activities_ga_kwargs, weekly_activities
from strava.formatters import update_activity_name, format_property, apply_formatters, noop_formatter
from strava.utils import filter_unique_week_flag

from strava.utils.activity_common import ACTIVITY_TOTAL_INIT, ACTIVITY_TOTAL_FORMATTERS, ACTIVITY_COLUMNS, \
    add_metrics_to_activity, format_activity

_DAY_TITLE = ['## Monday', '## Tuesday', '## Wednesday', '## Thursday', '## Friday', '## Saturday', '## Sunday']
_TOTAL_FORMATTERS = {
    'period': noop_formatter,
    **ACTIVITY_TOTAL_FORMATTERS,
}

@click.command(name='report',
               help='Reports the activities of a given week with additional information.'
               )
@click.option('--current', '-c', is_flag=True, default=False,
              help='Get the current week activities')
@click.option('--last', '-l', is_flag=True, default=False,
              help='Get the last week activities')
@click.option('--calendar_week', '-cw', type=int, nargs=2,
              help='Get the activities for the specified week number.\n Need two arguments (week number, year) like: -wn 2 2021.')
@click.option('--ftp', type=int,
              help='Specify an FTP to overwrite strava FTP.')
@output_option()
@login_required
def get_report(output, current, last, calendar_week, ftp):
    # If no flag is set, we use --current.
    if filter_unique_week_flag(current, last, calendar_week) == 0:
        current = True

    ga_kwargs = activities_ga_kwargs(current, last, calendar_week)
    activities = api.get_activities(**ga_kwargs)
    activities.reverse()
    activity_ids = [a.get('id') for a in activities]

    # Title of the reporting
    calendar_week = datetime.datetime.strptime(activities[0].get('start_date'), '%Y-%m-%dT%H:%M:%SZ').isocalendar()[1]
    click.echo(f'# Week {calendar_week}\n'
               f'Workout types:   \n'
               '* bike: <placeholder>  \n'
               '* run: <placeholder>  \n'
               '* swim: <placeholder>  \n'
               '* strength: <placeholder>  \n')

    # Summary
    click.echo('## Summary')
    activity_buffer, activity_total = split_activity_and_total(activity_ids, ftp)
    activity_total['period'] = '<placeholder>'
    for (key, value) in activity_total.items():
        if value == 0:
            _TOTAL_FORMATTERS.pop(key)
    _format_report_total(activity_total, _TOTAL_FORMATTERS, output)

    weekly_activities(output=output, quiet=False, current=current, last=last, week_number=calendar_week)

    # Days
    activity_days = [datetime.datetime.strptime(a.get('start_date'), '%Y-%m-%dT%H:%M:%SZ').weekday() for a in activities]
    for ad in set(activity_days):
        index = [ad == activity_day for activity_day in activity_days]
        click.echo(f'\n{_DAY_TITLE[ad]}')
        for id in list(compress(activity_ids, index)):
            format_activity(activity_buffer[id])


def split_activity_and_total(activity_ids, ftp=None):
    activity_total = ACTIVITY_TOTAL_INIT.copy()
    activity_buffer = {}
    for i, activity_id in enumerate(activity_ids):
        # Gets the activity.
        activity = api.get_activity(activity_id)
        activity['name'] = update_activity_name(activity)

        # Save the activity in the buffer dict.
        tmp_activity, tmp_met_formatters, activity_total = add_metrics_to_activity(activity, activity_total, from_=None, to=None, ftp=ftp)
        activity_buffer[activity_id] = {
            'activity': tmp_activity,
            'met_formatters': tmp_met_formatters
        }

        # Adapts the totals.
        activity_total['total_tss'] += tmp_activity.get('tss')
        activity_total['total_time'] += tmp_activity.get('moving_time')

    # Return the buffer and the total.
    return activity_buffer, activity_total


@format_result(table_columns=ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_report_total(activity, formatters, output=None):
    return activity if output == OutputType.JSON.value else _as_table(activity, formatters)


def _as_table(activity, formatters):
    return [{'key': format_property(k), 'value': v} for k, v in apply_formatters(activity, formatters).items()]
