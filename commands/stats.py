import click

from api.athlete import get_athlete, get_stats
from decorators import login_required, output_option, format_result
from formatters import format_ytd_stats, format_recent_stats


@click.group()
def stats():
    pass


@stats.command()
@output_option()
@login_required
@format_result(headers=['type', 'count', 'distance', 'moving_time', 'elevation_gain'])
def ytd(output):
    athlete = get_athlete()
    athlete_id = athlete.get('id')
    result = get_stats(athlete_id)
    return result if output == 'json' else format_ytd_stats(result)


@stats.command()
@output_option()
@login_required
@format_result(headers=['type', 'count', 'distance', 'moving_time', 'elevation_gain'])
def recent(output):
    athlete = get_athlete()
    athlete_id = athlete.get('id')
    result = get_stats(athlete_id)
    return result if output == 'json' else format_recent_stats(result)
