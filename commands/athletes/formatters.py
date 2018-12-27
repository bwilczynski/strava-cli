from formatters import format_distance, format_seconds, format_elevation, format_activity_type


def format_stats(stats):
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


def format_athlete(athlete):
    def format_name():
        return f'{athlete.get("firstname")} {athlete.get("lastname")}'

    formatted_athlete = {
        'id': athlete.get('id'),
        'username': athlete.get('username'),
        'name': format_name(),
        'email': athlete.get('email')
    }

    return [{'key': k, 'value': v} for k, v in formatted_athlete.items()]
