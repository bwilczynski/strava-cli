import click

import api
from commands.athletes.formatters import format_stats, format_athlete
from decorators import login_required, output_option


@click.command('stats')
@output_option()
@login_required
def get_stats(output):
    athlete = api.get_athlete()
    athlete_id = athlete.get('id')
    result = api.get_stats(athlete_id)
    return format_stats(result, output=output)


@click.command('profile')
@output_option()
@login_required
def get_profile(output):
    result = api.get_athlete()
    return format_athlete(result, output=output)
