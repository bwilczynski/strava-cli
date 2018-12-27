import click

import api
from api import athlete
from commands.athletes.formatters import format_stats, format_athlete
from decorators import login_required, output_option, format_result


@click.command('stats')
@output_option()
@login_required
@format_result(table_columns=['type', 'count', 'distance', 'moving_time', 'elevation_gain'])
def get_stats(output):
    athlete = api.athlete.get_athlete()
    athlete_id = athlete.get('id')
    result = api.athlete.get_stats(athlete_id)
    return result if output == 'json' else format_stats(result)


@click.command('profile')
@output_option()
@login_required
@format_result(
    table_columns=['key', 'value'])
def get_profile(output):
    result = athlete.get_athlete()
    return result if output == 'json' else format_athlete(result)
