import click
from dateparser import parse

from strava import api
from strava.decorators import output_option, login_required, format_result, OutputType
from strava.formatters import (
    noop_formatter,
    format_date,
    format_seconds,
    format_distance,
    format_speed,
    format_activity_name,
    apply_formatters,
)
import strava.settings

_SUMMARY_ACTIVITY_COLUMNS = (
    "id",
    "start_date",
    "name",
    "moving_time",
    "distance",
    "average_speed",
)

_SUMMARY_ACTIVITY_FORMATTERS = {
    "id": noop_formatter,
    "start_date": format_date,
    "moving_time": format_seconds,
    "distance": format_distance,
    "average_speed": format_speed,
}


@click.command("activities")
@output_option()
@click.option("--quiet", "-q", is_flag=True, default=False)
@click.option("--page", "-p", default=1, type=int)
@click.option("--per_page", "-pp", default=30, type=int)
@click.option("--before", "-B")
@click.option("--after", "-A")
@click.option("--index", "-I", type=int)
@click.option("--imperial_units", "-i", is_flag=True, default=False)
@login_required
@format_result(table_columns=_SUMMARY_ACTIVITY_COLUMNS)
def get_activities(output, quiet, page, per_page, before, after, index, imperial_units):
    ga_kwargs = dict()
    if before:
        ga_kwargs["before"] = parse(before).timestamp()
    if after:
        ga_kwargs["after"] = parse(after).timestamp()

    if imperial_units:
        strava.settings.IMPERIAL_UNITS = True

    result = api.get_activities(page=page, per_page=per_page, **ga_kwargs)
    if index is not None:
        result = result[index : index + 1]
    return result if (quiet or output == OutputType.JSON.value) else _as_table(result)


def _as_table(result):
    return [_format_summary_activity(activity) for activity in result]


def _format_summary_activity(activity):
    def format_name(name, activity):
        return format_activity_name(name, activity)

    formatters = {"name": format_name, **_SUMMARY_ACTIVITY_FORMATTERS}

    return apply_formatters(activity, formatters)
