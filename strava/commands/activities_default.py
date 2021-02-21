import click

from dateparser import parse

from strava import api
from strava.decorators import output_option, login_required, format_result, OutputType
from strava.utils.activities_common import as_table, SUMMARY_ACTIVITY_COLUMNS


@click.command(name='list',
               help='List all the recent activities.'
               )
@output_option()
@click.option('--quiet', '-q', is_flag=True, default=False,
              help='Keep it quiet.')
@click.option('--page', '-p', default=1, type=int,
              help='Page number. Defaults to 1.')
@click.option('--per_page', '-pp', default=30, type=int,
              help='Number of items per page. Defaults to 30.')
@click.option('--before', '-B',
              help='An epoch timestamp to use for filtering activities that have taken place before a certain time.')
@click.option('--after', '-A',
              help='An epoch timestamp to use for filtering activities that have taken place after a certain time.')
@click.option('--index', '-I', type=int,
              help='To only display specific index.')
@login_required
@format_result(table_columns=SUMMARY_ACTIVITY_COLUMNS)
def get_all_activities(output, quiet, page, per_page, before, after, index):
    ga_kwargs = dict()
    if before:
        ga_kwargs['before'] = parse(before).timestamp()
    if after:
        ga_kwargs['after'] = parse(after).timestamp()

    result = api.get_activities(page=page, per_page=per_page, **ga_kwargs)

    if index is not None:
        result = result[index:index + 1]
    return result if (quiet or output == OutputType.JSON.value) else as_table(result)
