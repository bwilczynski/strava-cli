import click

import api.activity
from api import athlete
from decorators import output_option, login_required
from .formatters import format_activities_result, format_activity_result


@click.command('activities')
@click.option('--page', '-p', default=1, type=int)
@click.option('--per_page', '-pp', default=30, type=int)
@click.option('--quiet', '-q', is_flag=True, default=False)
@output_option()
@login_required
def get_activities(output, quiet, page=1, per_page=30):
    result = athlete.get_activities(page, per_page)
    index_offset = (page - 1) * per_page + 1
    format_activities_result(result, index_offset, output=output, quiet=quiet)


@click.command('activity')
@click.option('--index', '-i', default=1, type=int)
@click.argument('activity_ids', required=False, nargs=-1)
@output_option()
@login_required
def get_activity(index, output, activity_ids):
    if activity_ids is None:
        activities = athlete.get_activities(index, 1)
        activity = activities[-1]
        activity_ids = [activity.get('id')]

    for i, activity_id in enumerate(activity_ids):
        if i > 0:
            click.echo()
        result = api.activity.get_activity(activity_id)
        format_activity_result(result, output)
