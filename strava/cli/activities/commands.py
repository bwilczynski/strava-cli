import click

from strava.commands import get_activities, get_weekly_activities


@click.group(name='activities', help='Get a list of recent activities.')
def cli_activities():
    pass


cli_activities.add_command(get_activities)
cli_activities.add_command(get_weekly_activities)
