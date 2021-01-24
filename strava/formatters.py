import os

import math
import re
from datetime import datetime, timezone

import click
from strava import emoji

N_A = 'N/A'


def format_seconds(seconds):
    if seconds > 3600:
        mins = math.floor(seconds / 60)
        return f'{math.floor(mins / 60):.0f}h {mins % 60:.0f}m'
    else:
        return f'{math.floor(seconds / 60):02.0f}:{seconds % 60:02.0f}'


def format_date(date):
    utc_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    return utc_date.replace(tzinfo=timezone.utc).astimezone()


def format_distance(distance):
    distance_km = math.floor(distance / 10) / 100
    return f'{distance_km:.2f} km' if distance_km > 0 else ''


def format_speed(speed):
    return f'{format_seconds(1000 / speed)} /km' if speed > 0 else None


def format_heartrate(heartrate):
    return f'{heartrate:.0f} bpm'


def format_activity_type(activity_type):
    return activity_type


def format_elevation(elevation):
    return f'{round(elevation)} m' if elevation > 0 else ''


def humanize(word):
    word = word.replace('_', ' ')
    word = re.sub(r"(?i)([a-z\d]*)", lambda m: m.group(1).lower(), word)
    word = re.sub(r"^\w", lambda m: m.group(0).upper(), word)
    return word


def noop_formatter(value):
    return value


def format_activity_name(name, activity):
    is_race = activity.get('workout_type', 0) == 1
    return f'{click.style(name, bold=is_race)}'


def update_activity_name(activity):
    name = activity.get('name')
    description = activity.get('description')
    return f"{name}{os.linesep}{description}" if description is not None else name

#def format_name(name, activity):
#    activity_name = format_activity_name(name, activity)
#    activity_description = activity.get('description')
#    return f"{activity_name}{os.linesep}{activity_description}" if activity_description is not None \
#        else activity_name


def format_gear(gear):
    return f'{gear.get("name")} ({format_distance(gear.get("distance", 0))})'


def format_heartrate_with_emoji(heartrate):
    return f"{click.style(emoji.RED_HEART, fg='red')} {format_heartrate(heartrate)}"


def format_speed_with_emoji(speed):
    return f"{click.style(emoji.RUNNING_SHOE, fg='yellow')} {format_speed(speed)}"


def format_elevation_with_emoji(elevation):
    if elevation is None:
        return ''
    else:
        difference = round(elevation)
    arrow = emoji.UP_ARROW if difference > 0 else emoji.DOWN_ARROW if difference < 0 else emoji.RIGHT_ARROW
    return f"{arrow} {format_elevation(abs(elevation))}"


def format_split(split):
    average_heartrate = format_heartrate_with_emoji(split['average_heartrate']) \
        if 'average_heartrate' in split else ''
    average_speed = format_speed_with_emoji(split['average_speed']) \
        if 'average_speed' in split else ''
    elevation_difference = format_elevation_with_emoji(split['elevation_difference']) \
        if 'elevation_difference' in split else ''
    return f'{average_speed} {average_heartrate} {elevation_difference}'


def format_property(name):
    return click.style(f'{humanize(name)}:', bold=True)


def format_power(power):
    if power is None:
        return ''
    return f'{power} W'


def format_cadence(cadence):
    if cadence is None:
        return ''
    return f'{cadence} rpm'


def apply_formatters(activity, formatters):
    return {k: formatter(activity[k]) if k in activity else N_A for k, formatter in formatters.items()}
