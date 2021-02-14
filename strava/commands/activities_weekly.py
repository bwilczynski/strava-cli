import click

from strava import api
from strava.decorators import output_option, login_required, format_result, OutputType
from strava.utils.time import activities_ga_kwargs, filter_unique_week_flag
from strava.utils.activities_common import as_table, SUMMARY_ACTIVITY_COLUMNS


@click.command(name='week',
               help='List the activities of a given week.'
               )
@output_option()
@click.option('--quiet', '-q', is_flag=True, default=False,
              help='Keep the command quiet.')
@click.option('--current', '-c', is_flag=True, default=False,
              help='[DEFAULT] Get the current week activities')  # It's tricky, this is set in the function itself
@click.option('--last', '-l', is_flag=True, default=False,
              help='Get the last week activities')
@click.option('--calendar_week', '-cw', type=int, nargs=2,
              help='Get the activities for the specified calendar week.\n Need two arguments (week number, year) like: -cw 2 2021.')
@login_required
def get_weekly_activities(output, quiet, current, last, calendar_week):
    weekly_activities(output, quiet, current, last, calendar_week)


@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def weekly_activities(output, quiet, current, last, calendar_week):
    # If no flag is set, we use --current.
    if filter_unique_week_flag(current, last, calendar_week) == 0:
        current = True

    ga_kwargs = activities_ga_kwargs(current, last, calendar_week)
    result = api.get_activities(**ga_kwargs)
    result.reverse()

    return result if (quiet or output == OutputType.JSON.value) else as_table(result)
