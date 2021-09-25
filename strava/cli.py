import click

from strava.commands import (
    login,
    logout,
    get_activities,
    get_activity,
    get_profile,
    get_stats,
    set_config,
    post_upload,
)


@click.group()
@click.version_option(package_name="strava-cli")
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(get_activities)
cli.add_command(get_activity)
cli.add_command(get_profile)
cli.add_command(get_stats)
cli.add_command(set_config)
cli.add_command(post_upload)

if __name__ == "__main__":
    cli()
