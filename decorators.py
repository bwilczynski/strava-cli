import functools
import json

import click
from click import option
from tabulate import tabulate

from config import creds_store


def format_result(headers=None, single=False):
    def decorator_format_result(func):
        @functools.wraps(func)
        def wrapper_format_result(*args, **kwargs):
            def print_json(data):
                prettified = json.dumps(data, indent=2, sort_keys=True)
                click.echo(prettified)

            def print_table(data):
                table_data = [data] if single else data
                rows = [[row[header] for header in headers] for row in table_data]
                click.echo(tabulate(rows, headers=headers))

            if 'output' in kwargs:
                output = kwargs['output']
                del kwargs['output']
            else:
                output = 'table'

            raw, formatted = func(*args, **kwargs)
            if output == 'json':
                print_json(formatted)
            elif output == 'raw':
                print_json(raw)
            else:
                print_table(formatted)

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
