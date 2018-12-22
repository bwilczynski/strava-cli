import functools
import json

import click
import requests
from click import option
from oauthlib.oauth2 import TokenExpiredError
from tabulate import tabulate

from config import creds_store
from config.creds_store import save_access_token
from settings import REFRESH_TOKEN_URL, STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET


def format_result(headers, single=False):
    def decorator_format_result(func):
        @functools.wraps(func)
        def wrapper_format_result(*args, **kwargs):
            def print_json():
                prettified = json.dumps(data, indent=2, sort_keys=True)
                click.echo(prettified)

            def print_table():
                table_data = [data] if single else data
                rows = [[row[header] for header in headers] for row in table_data]
                click.echo(tabulate(rows, headers=headers))

            if 'output' in kwargs:
                output = kwargs['output']
                del kwargs['output']
            else:
                output = 'table'

            data = func(*args, **kwargs)
            if output == 'json':
                print_json()
            else:
                print_table()

        return wrapper_format_result

    return decorator_format_result


def output_option(*args, **kwargs):
    def decorator_output_option(func):
        kwargs.setdefault('default', 'table')
        return option(*(args or ('--output', '-o',)), **kwargs)(func)

    return decorator_output_option


def login_required(func):
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if creds_store.get_access_token() is None:
            click.echo('Not logged in! Run `strava login` first.')
            return None
        return func(*args, **kwargs)

    return wrapper_login_required


def auto_refresh_token(client):
    def decorator_auto_refresh_token(func):
        @functools.wraps(func)
        def wrapper_auto_refresh_token(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TokenExpiredError:
                token = client.refresh_token(REFRESH_TOKEN_URL,
                                             auth=requests.auth.HTTPBasicAuth(STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET))
                client.token = token
                save_access_token(token)
                return func(*args, **kwargs)

        return wrapper_auto_refresh_token

    return decorator_auto_refresh_token
