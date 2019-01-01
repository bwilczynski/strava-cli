import click

from strava.config import creds_store


@click.command()
def logout():
    creds_store.delete_access_token()
