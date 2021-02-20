import click

from strava.commands import get_zones_heartrate, get_zones_power


@click.group(name='zones', help='[GROUP] Compute zone values from FTP test values.')
def cli_zones():
    pass


cli_zones.add_command(get_zones_heartrate)
cli_zones.add_command(get_zones_power)
