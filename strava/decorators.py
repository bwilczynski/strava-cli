import functools
import json
import os
from enum import Enum

import click
from click import option
from tabulate import tabulate

from strava import settings
from strava.config import creds_store
from strava.formatters import humanize


class OutputType(Enum):
    JSON = "json"
    TABLE = "table"


class TableFormat(Enum):
    SIMPLE = "simple"
    PLAIN = "plain"


def format_result(
    table_columns=None,
    single=False,
    show_table_headers=True,
    table_format=TableFormat.SIMPLE,
):
    def decorator_format_result(func):
        @functools.wraps(func)
        def wrapper_format_result(*args, **kwargs):
            def print_json(data):
                prettified = json.dumps(data, indent=2, sort_keys=True)
                click.echo(prettified)

            def print_table(data):
                table_data = [data] if single else data
                rows = [[row[header] for header in table_columns] for row in table_data]
                output = kwargs.get("output")
                tablefmt = table_format.value
                if output.index("table") == 0:
                    suffix = output.removeprefix("table")
                    if suffix.startswith("+"):
                        tablefmt = suffix[1:]
                click.echo(
                    tabulate(
                        rows,
                        headers=(humanize(header) for header in table_columns)
                        if show_table_headers
                        else (),
                        tablefmt=tablefmt,
                    )
                )

            def print_quiet(data):
                ids = [str(x.get("id")) for x in data]
                click.echo(os.linesep.join(ids))
                pass

            res = func(*args, **kwargs)

            if kwargs.get("quiet", False):
                print_res = print_quiet
            else:
                print_res = (
                    print_json
                    if kwargs.get("output") == OutputType.JSON.value
                    else print_table
                )

            print_res(res)

        return wrapper_format_result

    return decorator_format_result


def output_option(*args, **kwargs):
    def decorator_output_option(func):
        kwargs.setdefault("default", "table")
        return option(
            *(
                args
                or (
                    "--output",
                    "-o",
                )
            ),
            **kwargs
        )(func)

    return decorator_output_option


def login_required(func):
    @functools.wraps(func)
    def wrapper_login_required(*args, **kwargs):
        if creds_store.get_access_token() is None:
            click.echo("Not logged in! Run `strava login` first.")
            return None
        return func(*args, **kwargs)

    return wrapper_login_required


def config_required(func):
    @functools.wraps(func)
    def wrapper_config_required(*args, **kwargs):
        if settings.STRAVA_CLIENT_ID is None or settings.STRAVA_CLIENT_SECRET is None:
            click.echo(
                "Not configured. "
                "Run `strava config` or set environment "
                "variables STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET."
            )
            return None
        return func(*args, **kwargs)

    return wrapper_config_required
