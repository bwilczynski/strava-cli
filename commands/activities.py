import click

from api import activities
from decorators import login_required, format_result, output_option
from formatters import format_activity


@click.command('activities')
@click.option('--page', '-p', default=1, type=int)
@click.option('--per_page', '-pp', default=30, type=int)
@output_option()
@login_required
@format_result(
    headers=['start_date', 'name', 'distance', 'elapsed_time', 'average_speed', 'max_speed',
             'average_heartrate',
             'max_heartrate'])
def get_activities(page, per_page):
    result = activities.get(page, per_page)
    return result, [format_activity(activity) for activity in result]
