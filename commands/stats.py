import click

import api
from decorators import login_required, output_option, format_result
from formatters import format_distance, format_seconds, format_elevation, format_activity_type


@click.command('stats')
@output_option()
@login_required
@format_result(table_columns=['type', 'count', 'distance', 'moving_time', 'elevation_gain'])
def get_stats(output):
    athlete = api.athlete.get_athlete()
    athlete_id = athlete.get('id')
    result = api.athlete.get_stats(athlete_id)
    return result if output == 'json' else _format_stats(result)


def _format_stats(stats):
    formatters = {
        'count': lambda x: x,
        'distance': format_distance,
        'moving_time': format_seconds,
        'elevation_gain': format_elevation
    }

    def format_totals(totals):
        return {k: formatter(totals.get(k)) for k, formatter in formatters.items()}

    activity_types = ['run', 'ride', 'swim']
    total_types = ['recent', 'ytd', 'all']
    activity_totals = [(activity_type, total_type) for activity_type in activity_types for
                       total_type in total_types]

    return [
        dict(format_totals(stats[f'{total_type}_{activity_type}_totals']),
             **dict(type=f'{format_activity_type(activity_type)} {total_type}'))
        for activity_type, total_type in activity_totals
    ]
