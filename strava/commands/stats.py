import click

from strava import api
from strava.decorators import output_option, login_required, format_result, OutputType
from strava.formatters import (
    format_distance,
    format_seconds,
    format_elevation,
    format_activity_type,
)

import strava.settings

_STATS_COLUMNS = ("type", "count", "distance", "moving_time", "elevation_gain")


@click.command("stats")
@click.option("--imperial_units", "-i", is_flag=True, default=False)
@output_option()
@login_required
@format_result(table_columns=_STATS_COLUMNS)
def get_stats(output, imperial_units):
    if imperial_units:
        strava.settings.IMPERIAL_UNITS = True

    athlete = api.get_athlete()
    athlete_id = athlete.get("id")
    result = api.get_stats(athlete_id)
    return result if output == OutputType.JSON.value else _as_table(result)


def _as_table(stats):
    formatters = {
        "count": lambda x: x,
        "distance": format_distance,
        "moving_time": format_seconds,
        "elevation_gain": format_elevation,
    }

    def format_totals(totals):
        return {k: formatter(totals.get(k)) for k, formatter in formatters.items()}

    activity_types = ["run", "ride", "swim"]
    total_types = ["recent", "ytd", "all"]
    activity_totals = [
        (activity_type, total_type)
        for activity_type in activity_types
        for total_type in total_types
    ]

    return [
        dict(
            format_totals(stats[f"{total_type}_{activity_type}_totals"]),
            **dict(type=f"{format_activity_type(activity_type)} {total_type}"),
        )
        for activity_type, total_type in activity_totals
    ]
