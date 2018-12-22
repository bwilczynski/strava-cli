import click

from api import activities
from decorators import login_required, format_result, output_option


@click.command()
@output_option()
@format_result(headers=['start_date', 'distance'])
@login_required
def get_activities():
    return activities.get()
