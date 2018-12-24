import click

from api.athlete import get_athlete, get_stats
from decorators import login_required, output_option, format_result
from formatters import format_yearly_stats


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
    return result if output == 'json' else format_yearly_stats(result)
