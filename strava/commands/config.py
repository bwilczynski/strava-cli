import click

from strava.config import config_store


@click.command("config")
@click.option("--clear", is_flag=True)
def set_config(clear):
    if clear:
        config_store.delete_config()
        return

    click.echo("Please enter Strava application ID:")
    client_id = click.prompt("Client ID", type=int)
    client_secret = click.prompt("Client Secret", hide_input=True)

    config_store.save_config(dict(client_id=client_id, client_secret=client_secret))

    click.echo("Successfully configured Strava CLI.")
