from strava.formatters import noop_formatter, format_date, format_activity_type, format_seconds, format_distance, \
    update_activity_name, apply_formatters

SUMMARY_ACTIVITY_COLUMNS = (
    'id',
    'start_date',
    'type',
    'name',
    'moving_time',
    'distance',
)


_SUMMARY_ACTIVITY_FORMATTERS = {
    'id': noop_formatter,
    'start_date': format_date,
    'type': format_activity_type,
    'name': noop_formatter,
    'moving_time': format_seconds,
    'distance': format_distance,
}


def as_table(result):
    return [
        _format_summary_activity(activity) for
        activity in result]


def _format_summary_activity(activity):
    def format_name(name):
        return update_activity_name(name, activity)

    formatters = {
        'name': format_name,
        **_SUMMARY_ACTIVITY_FORMATTERS
    }

    return apply_formatters(activity, formatters)
