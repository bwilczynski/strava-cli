import click

from commands import login, logout, get_activities


@click.group()
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(get_activities)

if __name__ == '__main__':
    cli()
