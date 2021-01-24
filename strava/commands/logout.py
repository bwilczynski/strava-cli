import click

from strava.config import creds_store


@click.command(name='logout',
               help='Delete the current access token to logout of the strava account.'
               )
def logout():
    creds_store.delete_access_token()
