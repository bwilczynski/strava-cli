import datetime
import shelve
import pandas as pd
from dateparser import parse
import click
from strava.formatters import noop_formatter, format_property, apply_formatters

from strava.decorators import output_option, login_required, OutputType, format_result, TableFormat

from strava.config.local_store import _get_fullpath

from strava import api
from strava.utils.form import get_tss_entry, compute_daily_tss, compute_CTL, compute_ATL

_FORM_COLUMNS = ('key', 'value')


@click.command(name='form',
               help='Provide the fitness, fatigue and form for a given day.'
               )
@click.option('--date', '-d', type=str, default='today',
              help="The date for which fitness, fatigue and form should be computed. By default is today.")
@output_option()
@login_required
def get_form(output, date):
    formatted_date = parse(date).date()
    return get_form_with_formatted_date(output, formatted_date)


def get_form_with_formatted_date(output, date):
    CTL, ATL, TSB = compute_fitness_fatigue_form(date)
    result = {
        'Fitness (CTL)': CTL,
        'Fatigue (ATL)': ATL,
        'Form (TSB)': TSB,
    }
    return result if output == OutputType.JSON.value else _format_result(result)


def compute_fitness_fatigue_form(date=datetime.datetime.today().date()):
    end = datetime.datetime(date.year, date.month, date.day) + datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=42)
    act_in_window = api.get_activities(per_page=100, before=end.timestamp(), after=start.timestamp())
    ids_in_window = [a.get('id') for a in act_in_window]

    cache = shelve.open(_get_fullpath('cache'))
    tss_list = []
    for act_id in ids_in_window:
        id_str = str(act_id)
        if id_str in cache:
            tss_entry = cache[id_str]
            tss_list.append(tss_entry)
        else:
            tss_entry = get_tss_entry(act_id)
            cache[id_str] = tss_entry
            tss_list.append(tss_entry)
    cache.close()
    daily_tss = compute_daily_tss(tss_list)

    delta = end - start
    tss_table = pd.DataFrame(columns=('date', 'tss'))
    for i in range(delta.days + 1):
        day = start + datetime.timedelta(days=i)
        st_day = day.strftime('%Y-%m-%d')
        if st_day in daily_tss.keys():
            tss_entry = daily_tss[st_day]
        else:
            tss_entry = 0
        tss_table = tss_table.append({'date': st_day, 'tss': tss_entry}, ignore_index=True)

    CTL = compute_CTL(tss_table)
    ATL = compute_ATL(tss_table)
    TSB = CTL - ATL

    return CTL, ATL, TSB


@format_result(table_columns=_FORM_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_result(result, output=None):
    formatters = {
        'Fitness (CTL)': noop_formatter,
        'Fatigue (ATL)': noop_formatter,
        'Form (TSB)': noop_formatter,
    }
    return result if output == OutputType.JSON.value else _as_table(result, formatters)


def _as_table(result, formatters):
    return [{'key': format_property(k), 'value': v} for k, v in apply_formatters(result, formatters).items()]
