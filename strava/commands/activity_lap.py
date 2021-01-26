import click

from strava import api
from strava.commands.activity_default import get_activity_from_ids
from strava.decorators import output_option, login_required
from strava.utils.activity_common import get_lap

_ACTIVITY_COLUMNS = ('key', 'value')


@click.command(name='laps',
               help='Display metrics for each registered lap.'
               )
@click.argument('activity_id', required=True, nargs=1)
@click.option('--ftp', type=int,
              help='Specify an FTP to overwrite strava FTP.')
@output_option()
@login_required
def get_lap_activity(output, activity_id, ftp):
    activity = api.get_activity(activity_id)

    # Display main information.
    get_activity_from_ids(output, activity_ids=[activity_id], details=True, total=False, ftp=ftp)
    click.echo()

    # Display laps information.
    for lap in range(0, len(activity.get('laps'))):
        get_lap(output, activity=activity, lap=lap, ftp=ftp)
        click.echo()
