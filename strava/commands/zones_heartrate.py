import math
import click

from strava.decorators import format_result

_ZONES_COLUMNS = (
    'zone',
    'heartrate'
)

@click.command(name='heartrate',
               help='Generate heartrate zones and FTHR according to the 20 minutes averaged value provided.')
@click.argument('heartrate', required=True, nargs=1, type=int)
@format_result(table_columns=_ZONES_COLUMNS)
def get_zones_heartrate(heartrate):
    fthr = math.ceil(heartrate * 0.95)
    hr_zone1_up = round(heartrate*0.81)
    hr_zone2_up = round(heartrate*0.89)
    hr_zone3_up = round(heartrate*0.93)
    hr_zone4_up = round(heartrate*0.99)
    hr_zone5_up = round(heartrate*1.02)
    hr_zone6_up = round(heartrate*1.06)
    fthr_table = {
        'FTHR': fthr,
        '---': '---',
        '1 (<81%)': f'<{hr_zone1_up}',
        '2 (82%-89%)': f'{hr_zone1_up + 1}-{hr_zone2_up}',
        '3 (90%-93%)': f'{hr_zone2_up + 1}-{hr_zone3_up}',
        '4 (94%-99%)': f'{hr_zone3_up + 1}-{hr_zone4_up}',
        '5 (100%-102%)': f'{hr_zone4_up + 1}-{hr_zone5_up}',
        '6 (103%-106%)': f'{hr_zone5_up + 1}-{hr_zone6_up}',
        '7 (>107%)': f'>{hr_zone6_up + 1}',
    }

    return _as_table(fthr_table)


def _as_table(table):
    return [{'zone': k, 'heartrate': v} for k, v in table.items()]
