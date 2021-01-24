import click

from strava import api
from strava.decorators import output_option, login_required, format_result, OutputType
from strava.utils.time import activities_ga_kwargs
from strava.utils.activities_common import as_table, SUMMARY_ACTIVITY_COLUMNS


@click.command(name='week',
               help='List the activities of a given week.'
               )
@output_option()
@click.option('--quiet', '-q', is_flag=True, default=False,
              help='Keep the command quiet.')
@click.option('--current', '-c', is_flag=True, default=False,
              help='Get the current week activities')
@click.option('--last', '-l', is_flag=True, default=False,
              help='Get the last week activities')
@click.option('--week_number', '-wn', type=int, nargs=2,
              help='Get the activities for the specified week number.\n Need two arguments (week number, year) like: -wn 2 2021.')
@login_required
@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def get_weekly_activities(output, quiet, current, last, week_number):
    ga_kwargs = activities_ga_kwargs(current, last, week_number)
    result = api.get_activities(**ga_kwargs)
    result.reverse()

    return result if (quiet or output == OutputType.JSON.value) else as_table(result)
