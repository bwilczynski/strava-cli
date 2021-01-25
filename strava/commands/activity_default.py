import click

from strava.decorators import output_option, login_required
from strava.utils import get_activity_from_ids


@click.command(name='list',
               help='List and display all the recent activities with additional information.'
               )
@click.argument('activity_ids', required=False, nargs=-1)
@click.option('--details', '-d', default=False, is_flag=True,
              help='Get more details about an activity.\n Enable advanced metrics computation.')
@click.option('--total', '-t', default=False, is_flag=True,
              help='Indicates whenever the total should be computed.\n Only available with multiple ids. Will set --details to True.')
@click.option('--ftp', type=int,
              help='Specify an FTP to overwrite strava FTP.')
@output_option()
@login_required
def get_activity(output, activity_ids, details, total, ftp):
    return get_activity_from_ids(output, activity_ids, details, total, ftp=ftp)
