import click

from strava import api
from strava.decorators import output_option, login_required, format_result, OutputType

_PROFILE_COLUMNS = ("key", "value")


@click.command("profile")
@output_option()
@login_required
@format_result(table_columns=_PROFILE_COLUMNS)
def get_profile(output):
    result = api.get_athlete()
    return result if output == OutputType.JSON.value else _as_table(result)


def _as_table(athlete):
    def format_name():
        return f'{athlete.get("firstname")} {athlete.get("lastname")}'

    formatted_athlete = {
        "id": athlete.get("id"),
        "username": athlete.get("username"),
        "name": format_name(),
        "email": athlete.get("email"),
    }

    return [{"key": k, "value": v} for k, v in formatted_athlete.items()]
