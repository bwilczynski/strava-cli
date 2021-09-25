import click

from strava import api
from strava.decorators import (
    output_option,
    login_required,
    format_result,
    TableFormat,
    OutputType,
)
from strava.formatters import (
    humanize,
    apply_formatters,
)
import time

_ACTIVITY_COLUMNS = ("key", "value")


@click.command("upload")
@click.argument("upload_files", required=True, nargs=-1)
@output_option()
@login_required
def post_upload(output, upload_files):
    for i, filename in enumerate(upload_files):
        if i > 0:
            click.echo()
        if i % 90 == 0 and i > 5:
            click.echo(f"Sleeping for API rate limiting, uploaded {i} items.")
            time.sleep(900)
            # Can only perform 100 API requests every 15 minutes # noqa: E501
            # so we'll do 90 then sleep, to allow for reads that may happen in other threads # noqa: E501
            # http://developers.strava.com/docs/#rate-limiting # noqa: E501
            # the api/upload/py post_upload() code *should* catch this, sleep, and retry itself # noqa: E501
            # but the included requests module isn't returning the error code to trap the 429. # noqa: E501
        xargs = _process_file(filename)
        if xargs is None:
            # file isn't XML, have to bail
            result = None
        else:
            result = api.post_upload(xargs, filename)
        _format_upload(result, output=output)


@format_result(
    table_columns=_ACTIVITY_COLUMNS,
    show_table_headers=False,
    table_format=TableFormat.PLAIN,
)
def _format_upload(result, output=None):
    return result if output == OutputType.JSON.value else _as_table(result)


def _as_table(upload_result):
    def format_id(upload_id):
        return f"{upload_id}"

    def format_error(upload_error):
        return f"{upload_error}"

    def format_status(upload_status):
        return f"{upload_status}"

    def format_property(name):
        return click.style(f"{humanize(name)}:", bold=True)

    formatters = {
        "id": format_id,
        "status": format_status,
        "error": format_error,
    }

    basic_data = [
        {"key": format_property(k), "value": v}
        for k, v in apply_formatters(upload_result, formatters).items()
    ]

    return [*basic_data]


def _process_file(filename):
    import xml.etree.ElementTree as ElementTree
    import re

    try:
        activity_tree = ElementTree.parse(filename)
        activity_root = activity_tree.getroot()
    except ElementTree.ParseError:
        # not an XML file - there might be junk in the directory
        return None
    params = {}
    typere = re.search(r"\}([a-z.]{3,6})$", activity_root.tag)
    if typere:
        params.update({"data_type": typere.group(1)})
    try:
        if re.search(r"\}name$", activity_root[0][0].tag):
            params.update({"name": activity_root[0][0].text})
            activity_match = re.search(r"(?i)^([a-z]*)\s", activity_root[0][0].text)
            if activity_match:
                activitytype = str(activity_match.group(1)).strip().lower()
                if activitytype == "skating":
                    activitytype = "inlineskate"
                if activitytype == "downhill":
                    activitytype = "alpineski"
                if activitytype == "hiking":
                    activitytype = "hike"
                if activitytype == "running":
                    activitytype = "run"
                if activitytype == "cycling":
                    activitytype = "ride"
                if activitytype == "walking":
                    activitytype = "walk"
                if activitytype == "swimming":
                    activitytype = "swim"
                if activitytype == "sport":
                    activitytype = "workout"
                params.update({"activity_type": activitytype})

    except IndexError:
        # This tag doesn't exist, it's not RunKeeper format GPX
        # so some other format defines the definition. TODO
        # So we'll try to upload it without any values
        ...
    return params
