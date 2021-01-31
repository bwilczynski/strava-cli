import click
import datetime
from itertools import compress

from strava import api
from strava.commands.activity_default import get_activity_from_ids
from strava.decorators import output_option, login_required
from strava.commands.activities_weekly import activities_ga_kwargs

_DAY_TITLE = ['## Monday', '## Tuesday', '## Wednesday', '## Thursday', '## Friday', '## Saturday', '## Sunday']

@click.command(name='week',
               help='List and display the activities of a given week with additional information.'
               )
@click.option('--details', '-d',
              help='Get more details about an activity.\n Enable advanced metrics computation.', default=False, is_flag=True)
@click.option('--total', '-t', default=False, is_flag=True,
              help='Indicates whenever the total should be computed.\n Only available with multiple ids. Will set --details to True.')
@click.option('--report', '-r', default=False, is_flag=True,
              help='True if it is to have the week as a markdown report.')
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
def get_weekly_activity(output, details, total, report, current, last, week_number, ftp):
    ga_kwargs = activities_ga_kwargs(current, last, week_number)
    activities = api.get_activities(**ga_kwargs)
    activities.reverse()
    activity_ids = [a.get('id') for a in activities]

    if report:
        week_number = datetime.datetime.strptime(activities[0].get('start_date'), '%Y-%m-%dT%H:%M:%SZ').isocalendar()[1]
        click.echo(f'# Week {week_number}')

        activity_days = [datetime.datetime.strptime(a.get('start_date'), '%Y-%m-%dT%H:%M:%SZ').weekday() for a in activities]
        for ad in set(activity_days):
            index = [ad == activity_day for activity_day in activity_days]
            click.echo(f'\n{_DAY_TITLE[ad]}')
            get_activity_from_ids(output=output, activity_ids=list(compress(activity_ids, index)), details=details, total=False, ftp=ftp)

        if total:
            get_activity_from_ids(output=output, activity_ids=activity_ids, details=False, total=total, ftp=ftp)
    else:
        get_activity_from_ids(output=output, activity_ids=activity_ids, details=details, total=total, ftp=ftp)
