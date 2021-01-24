import click

from strava.commands import get_activity, get_range_activity, get_weekly_activity


@click.group(name='activity', help='Get the summary of one or multiple activities.')
def cli_activity():
    pass


cli_activity.add_command(get_activity)
cli_activity.add_command(get_range_activity)
cli_activity.add_command(get_weekly_activity)
