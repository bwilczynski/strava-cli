import click

from strava.commands import login, logout, get_profile, get_stats, set_config, post_upload, get_cw
from strava.cli.activity import commands as activity
from strava.cli.activities import commands as activities


@click.group()
@click.version_option()
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(get_profile)
cli.add_command(get_stats)
cli.add_command(set_config)
cli.add_command(post_upload)
cli.add_command(get_cw)

cli.add_command(activity.cli_activity)
cli.add_command(activities.cli_activities)


if __name__ == '__main__':
    cli()
