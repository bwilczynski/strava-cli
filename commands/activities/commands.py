import click
from dateparser import parse

import api
from decorators import output_option, login_required
from .formatters import format_activities, format_activity


@click.command('activities')
@output_option()
@click.option('--quiet', '-q', is_flag=True, default=False)
@click.option('--page', '-p', default=1, type=int)
@click.option('--per_page', '-pp', default=30, type=int)
@click.option('--before', '-B')
@click.option('--after', '-A')
@login_required
def get_activities(output, quiet, page=None, per_page=None, before=None, after=None):
    ga_kwargs = dict()
    if before:
        ga_kwargs['before'] = parse(before).timestamp()
    if after:
        ga_kwargs['after'] = parse(after).timestamp()

    result = api.get_activities(page=page, per_page=per_page, **ga_kwargs)
    format_activities(result, output=output, quiet=quiet)


@click.command('activity')
@click.argument('activity_ids', required=True, nargs=-1)
@output_option()
@login_required
def get_activity(output, activity_ids=None):
    for i, activity_id in enumerate(activity_ids):
        if i > 0:
            click.echo()
        result = api.get_activity(activity_id)
        format_activity(result, output=output)
