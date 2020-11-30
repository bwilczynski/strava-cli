import os

import click

from strava import api, emoji
from strava.decorators import output_option, login_required, format_result, TableFormat, OutputType
from strava.formatters import humanize, noop_formatter, \
    format_date, format_seconds, apply_formatters

_ACTIVITY_COLUMNS = ('key', 'value')


@click.command('upload')
@click.argument('upload_files', required=True, nargs=-1)
@output_option()
@login_required
def post_upload(output, upload_files):
    for i, filename in enumerate(upload_files):
        if i > 0:
            click.echo()
        xargs = _process_file(filename)
        if xargs is None:
            # file isn't XML, have to bail
            result = None
        else:
            result=None
            with open(filename, 'rb') as f:
                xargs.update({'file':f})
                result = api.post_upload(xargs)
        _format_upload(result, output=output)


@format_result(table_columns=_ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_upload(result, output=None):
    return result if output == OutputType.JSON.value else _as_table(result)


def _as_table(upload_result):
    def format_id(upload_id):
        return "{0}".format(upload_id)


    formatters = {
        'id': format_id,
        'status': noop_formatter,
        'error': noop_formatter,
    }

    basic_data = [
        {'key': format_property(k), 'value': v} for k, v in apply_formatters(activity, formatters).items()
    ]
    split_data = [
        {'key': format_property(f"Split {split.get('split')}"), 'value': format_split(split)} for split in
        activity.get('splits_metric', [])
    ]

    return [
        *basic_data,
        *split_data
    ]

def _process_file(filename):
    import xml.etree.ElementTree as ET
    import re
    try:
        activity_tree = ET.parse(filename)
        activity_root = activity_tree.getroot()
    except xml.etree.ElementTree.ParseError:
        # not an XML file - there might be junk in the directory
        return None
    params={}
    typere=re.search(r'\}([a-z.]{3,6})$', root.tag)
    if typere:
        params.update({'data_type': typere.group(1)})
    try:
        if re.search(r'\}name$', root[0][0].tag):
            params.update({'name': root[0][0].text})
    except IndexError:
        # This tag doesn't exist, it's not RunKeeper format GPX
        # so some other format defines the definition. TODO
        ...
    return params

