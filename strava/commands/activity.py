import os

import click

from strava import api, emoji
from strava.decorators import (
    output_option,
    login_required,
    format_result,
    TableFormat,
    OutputType,
)
from strava.formatters import (
    format_distance,
    format_heartrate,
    format_speed,
    format_elevation,
    humanize,
    noop_formatter,
    format_date,
    format_seconds,
    format_activity_name,
    apply_formatters,
)
import strava.settings

_ACTIVITY_COLUMNS = ("key", "value")


@click.command("activity")
@click.argument("activity_ids", required=True, nargs=-1)
@click.option("--imperial_units", "-i", is_flag=True, default=False)
@output_option()
@login_required
def get_activity(output, activity_ids, imperial_units):
    if imperial_units:
        strava.settings.IMPERIAL_UNITS = True

    for i, activity_id in enumerate(activity_ids):
        if i > 0:
            click.echo()
        result = api.get_activity(activity_id)
        _format_activity(result, output=output)


@format_result(
    table_columns=_ACTIVITY_COLUMNS,
    show_table_headers=False,
    table_format=TableFormat.PLAIN,
)
def _format_activity(result, output=None):
    return result if output == OutputType.JSON.value else _as_table(result)


def _as_table(activity):
    def format_name(name, activity=None):
        activity_name = format_activity_name(name, activity)
        activity_description = activity.get("description")
        return (
            f"{activity_name}{os.linesep}{activity_description}"
            if activity_description is not None
            else activity_name
        )

    def format_gear(gear):
        return f'{gear.get("name")} ({format_distance(gear.get("distance", 0))})'

    def format_heartrate_with_emoji(heartrate):
        return f"{click.style(emoji.RED_HEART, fg='red')} {format_heartrate(heartrate)}"

    def format_speed_with_emoji(speed):
        return f"{click.style(emoji.RUNNING_SHOE, fg='yellow')} {format_speed(speed, activity)}"

    def format_elevation_with_emoji(elevation):
        difference = round(elevation)
        arrow = (
            emoji.UP_ARROW
            if difference > 0
            else emoji.DOWN_ARROW
            if difference < 0
            else emoji.RIGHT_ARROW
        )
        return f"{arrow} {format_elevation(abs(elevation))}"

    def format_split(split):
        average_heartrate = (
            format_heartrate_with_emoji(split["average_heartrate"])
            if "average_heartrate" in split
            else ""
        )
        average_speed = (
            format_speed_with_emoji(split["average_speed"])
            if "average_speed" in split
            else ""
        )
        elevation_difference = (
            format_elevation_with_emoji(split["elevation_difference"])
            if "elevation_difference" in split
            else ""
        )
        return f"{average_speed} {average_heartrate} {elevation_difference}"

    def format_property(name):
        return click.style(f"{humanize(name)}:", bold=True)

    formatters = {
        "name": format_name,
        "start_date": format_date,
        "moving_time": format_seconds,
        "distance": format_distance,
        "average_speed": format_speed,
        "max_speed": format_speed,
        "average_heartrate": format_heartrate,
        "max_heartrate": format_heartrate,
        "total_elevation_gain": format_elevation,
        "calories": noop_formatter,
        "device_name": noop_formatter,
        "gear": format_gear,
    }

    basic_data = [
        {"key": format_property(k), "value": v}
        for k, v in apply_formatters(activity, formatters).items()
    ]
    split_data = [
        {
            "key": format_property(f"Split {split.get('split')}"),
            "value": format_split(split),
        }
        for split in activity.get("splits_metric", [])
    ]

    return [*basic_data, *split_data]
