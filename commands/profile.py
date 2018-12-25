import click

from api import athlete
from decorators import output_option, login_required, format_result


@click.command('profile')
@output_option()
@login_required
@format_result(
    table_columns=['key', 'value'])
def get_profile(output):
    result = athlete.get_athlete()
    return result if output == 'json' else _format_athlete(result)


def _format_athlete(athlete):
    def format_name():
        return f'{athlete.get("firstname")} {athlete.get("lastname")}'

    formatted_athlete = {
        'id': athlete.get('id'),
        'username': athlete.get('username'),
        'name': format_name(),
        'email': athlete.get('email')
    }

    return [{'key': k, 'value': v} for k, v in formatted_athlete.items()]
