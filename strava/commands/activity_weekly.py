import click

from strava import api
from strava.commands.activity_default import get_activity_from_ids
from strava.decorators import output_option, login_required
from strava.commands.activities_weekly import activities_ga_kwargs


@click.command(name='week',
               help='List and display the activities of a given week with additional information.'
               )
@click.option('--details', '-d',
              help='Get more details about an activity.\n Enable advanced metrics computation.', default=False, is_flag=True)
@click.option('--total', '-t', default=False, is_flag=True,
              help='Indicates whenever the total should be computed.\n Only available with multiple ids. Will set --details to True.')
@click.option('--current', '-c', is_flag=True, default=False,
              help='Get the current week activities')
@click.option('--last', '-l', is_flag=True, default=False,
              help='Get the last week activities')
@click.option('--week_number', '-wn', type=int, nargs=2,
              help='Get the activities for the specified week number.\n Need two arguments (week number, year) like: -wn 2 2021.')
@click.option('--ftp', type=int,
              help='Specify an FTP to overwrite strava FTP.')
@output_option()
@login_required
def get_weekly_activity(output, details, total, current, last, week_number, ftp):
    ga_kwargs = activities_ga_kwargs(current, last, week_number)
    activities = api.get_activities(**ga_kwargs)
    activities.reverse()
    activity_ids = [a.get('id') for a in activities]

    return get_activity_from_ids(output, activity_ids, details, total, ftp=ftp)
