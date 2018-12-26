import functools
import json

import click
from click import option
from tabulate import tabulate

from config import creds_store
from formatters import humanize


def format_result(table_columns=None, single=False, show_table_headers=True, table_format='simple'):
    def decorator_format_result(func):
        @functools.wraps(func)
        def wrapper_format_result(*args, **kwargs):
            def print_json(data):
                prettified = json.dumps(data, indent=2, sort_keys=True)
                click.echo(prettified)

            def print_table(data):
                table_data = [data] if single else data
                rows = [[row[header] for header in table_columns] for row in table_data]
                click.echo(
                    tabulate(rows,
                             headers=[humanize(header) for header in table_columns] if show_table_headers else [],
                             tablefmt=table_format))

            output = kwargs.get('output', 'table')
            res = func(*args, **kwargs)
            print_json(res) if output == 'json' else print_table(res)

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
