import sys

import click
import datetime


def activities_ga_kwargs(current, last, week_number):
    if not _filter_unique_week_flag(current, last, week_number):
        click.echo("Only one option from --current, --last and --week-number can be chosen at one time.")
        sys.exit()

    ga_kwargs = dict()
    if current:
        ga_kwargs['after'], ga_kwargs['before'] = _get_weekly_before_and_after()
    if last:
        ga_kwargs['after'], ga_kwargs['before'] = \
            _get_weekly_before_and_after(date=datetime.datetime.now().date()-datetime.timedelta(days=7))
    if week_number:
        ga_kwargs['after'], ga_kwargs['before'] = \
            _get_weekly_before_and_after(date=_monday_of_calenderweek(week_number[0], week_number[1]))
    return ga_kwargs


def input_tuple_to_secs(t):
    try:
        assert isinstance(t, tuple)
        return t[0]*3600 + t[1]*60 + t[2]
    except:
        click.echo('The time format is not as it should!')
        raise


def _filter_unique_week_flag(current, last, week_number):
    wn = 1 if week_number else 0
    return current + last + wn == 1


def _get_weekly_before_and_after(date=datetime.datetime.now().date()):
    start = date - datetime.timedelta(days=date.weekday())
    end = start + datetime.timedelta(days=7)
    start_epoch = datetime.datetime(start.year, start.month, start.day).timestamp()
    end_epoch = datetime.datetime(end.year, end.month, end.day).timestamp()
    return start_epoch, end_epoch


def _monday_of_calenderweek(week_number, year):
    first = datetime.date(year, 1, 1)
    base = 1 if first.isocalendar()[1] == 1 else 8
    return first + datetime.timedelta(days=base - first.isocalendar()[2] + 7 * (week_number - 1))
