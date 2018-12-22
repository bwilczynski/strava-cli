import click

from config.creds_store import delete_access_token


@click.command()
def logout():
    delete_access_token()
