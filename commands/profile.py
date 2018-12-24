import click

from api import athlete
from decorators import output_option, login_required, format_result
from formatters import format_athlete


@click.command()
@output_option()
@login_required
@format_result(
    headers=['key', 'value'])
def profile(output):
    result = athlete.get_athlete()
    return result if output == 'json' else format_athlete(result)
