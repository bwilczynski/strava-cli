import click

from strava.commands.activity_default import get_activity_from_ids
from strava.decorators import output_option, login_required

_ACTIVITY_COLUMNS = ('key', 'value')


@click.command(name='constrain',
               help='Constrain the time of the activity on both side for deeper analysis.'
               )
@click.argument('activity_id', required=True, nargs=1)
@click.option('--from', '-f', 'from_', nargs=3, type=int, default=None,
              help='Select the start time to narrow the computation to a specific part of the activity.\n If not select the start of the activity is used.\n Need to be entered as 3 numbers, first is the hours, second the minutes ans last the seconds.')
@click.option('--to', '-t', 'to', nargs=3, type=int, default=None,
              help='Select the end time to narrow the computation to a specific part of the activity.\n If not select the end of the activity is used.\n Need to be entered as 3 numbers, first is the hours, second the minutes ans last the seconds.')
@click.option('--ftp', type=int,
              help='Specify an FTP to overwrite strava FTP.')
@output_option()
@login_required
def get_range_activity(output, activity_id, from_, to, ftp):
    return get_activity_from_ids(output, activity_ids=[activity_id], details=True, total=False, from_=from_, to=to, ftp=ftp)
