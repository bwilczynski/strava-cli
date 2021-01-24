import click

from strava import api
from strava.decorators import output_option, login_required
from strava.formatters import update_activity_name
from strava.utils.activity_common import ACTIVITY_TOTAL_INIT, format_activity, \
    format_activity_total
from strava.utils.streams_ride import ride_detail
from strava.utils.streams_run import run_detail
from strava.utils.streams_workout import workout_detail


@click.command(name='list',
               help='List and display all the recent activities with additional information.'
               )
@click.argument('activity_ids', required=False, nargs=-1)
@click.option('--details', '-d', default=False, is_flag=True,
              help='Get more details about an activity.\n Enable advanced metrics computation.')
@click.option('--total', '-t', default=False, is_flag=True,
              help='Indicates whenever the total should be computed.\n Only available with multiple ids. Will set --details to True.')
@output_option()
@login_required
def get_activity(output, activity_ids, details, total):
    return get_activity_from_ids(output, activity_ids, details, total)


def get_activity_from_ids(output, activity_ids, details=False, total=False, from_=None, to=None):
    activity_total = ACTIVITY_TOTAL_INIT
    for i, activity_id in enumerate(activity_ids):
        if i > 0:
            click.echo()

        # Gets the activity.
        activity = api.get_activity(activity_id)
        activity['name'] = update_activity_name(activity)

        # Add details if asked.
        met_formatters = None
        if details or total:
            act_type = activity.get('type')
            if act_type == 'Ride' or act_type == 'VirtualRide':
                metrics, met_formatters = ride_detail(activity, from_, to)
            elif act_type == 'Run':
                metrics, met_formatters = run_detail(activity, from_, to)
            elif act_type == 'Workout':
                metrics, met_formatters = workout_detail(activity, from_, to)
            else:
                metrics = {'tss': 0}
            # Returns the details.
            activity.update(metrics)

        format_activity(activity, met_formatters, output=output)

        # Adapts totals.
        if total:
            activity_total['total_tss'] += activity.get('tss')
            activity_total['total_time'] += activity.get('moving_time')
            activity_total['number_of_activities'] += 1

    # Return the totals.
    if total:
        click.echo('\nTotal')
        format_activity_total(activity_total, output=output)
