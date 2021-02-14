import click

from strava import api
from strava.commands.activity_default import get_activity_from_ids
from strava.decorators import output_option, login_required
from strava.commands.activities_weekly import activities_ga_kwargs
from strava.utils import filter_unique_week_flag


@click.command(name='week',
               help='List and display the activities of a given week with additional information.'
               )
@click.option('--details', '-d',
              help='Get more details about an activity.\n Enable advanced metrics computation.', default=False, is_flag=True)
@click.option('--total', '-t', default=False, is_flag=True,
              help='Indicates whenever the total should be computed.\n Only available with multiple ids. Will set --details to True.')
@click.option('--current', '-c', is_flag=True, default=False,
              help='[DEFAULT] Get the current week activities')  # It's tricky, this is set in the function itself
@click.option('--last', '-l', is_flag=True, default=False,
              help='Get the last week activities')
@click.option('--calendar_week', '-cw', type=int, nargs=2,
              help='Get the activities for the specified calendar week.\n Need two arguments (week number, year) like: -cw 2 2021.')
@click.option('--ftp', type=int,
              help='Specify an FTP to overwrite strava FTP.')
@output_option()
@login_required
def get_weekly_activity(output, details, total, current, last, calendar_week, ftp):
    # If no flag is set, we use --current.
    if filter_unique_week_flag(current, last, calendar_week) == 0:
        current = True

    ga_kwargs = activities_ga_kwargs(current, last, calendar_week)
    activities = api.get_activities(**ga_kwargs)
    activities.reverse()
    activity_ids = [a.get('id') for a in activities]

    get_activity_from_ids(output=output, activity_ids=activity_ids, details=details, total=total, ftp=ftp)
