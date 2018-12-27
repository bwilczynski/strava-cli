import click

import api.activity
from api import athlete
from commands.activities.formatters import format_summary_activity, format_activity
from decorators import output_option, login_required, format_result

SUMMARY_ACTIVITY_COLUMNS = [
    'index',
    'start_date',
    'name',
    'distance',
    'elapsed_time',
    'average_speed',
    'max_speed',
    'average_heartrate',
    'max_heartrate'
]


@click.command('activities')
@click.option('--page', '-P', default=1, type=int)
@click.option('--per_page', '-PP', default=30, type=int)
@output_option()
@login_required
@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def get_activities(output, page=1, per_page=30):
    result = athlete.get_activities(page, per_page)
    return result if output == 'json' else [format_summary_activity(index + (page - 1) * per_page + 1, activity) for
                                            index, activity in
                                            enumerate(result)]


@click.command('activity')
@click.option('--index', '-I', default=1, type=int)
@output_option()
@login_required
@format_result(table_columns=['key', 'value'], show_table_headers=False, table_format='plain')
def get_activity(index, output):
    activities = athlete.get_activities(index, 1)
    activity = activities[-1]
    activity_id = activity.get('id')
    result = api.activity.get_activity(activity_id)
    return result if output == 'json' else format_activity(result)
