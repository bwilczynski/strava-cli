import math
import click

from strava.decorators import format_result

_ZONES_COLUMNS = (
    'zone',
    'power'
)

@click.command(name='power',
               help='Generate power zones and FTP according to the 20 minutes averaged value provided.')
@click.argument('power', required=True, type=int, nargs=1)
@format_result(table_columns=_ZONES_COLUMNS)
def get_zones_power(power):
    ftp = math.ceil(power * 0.95)
    zone1_up = round(ftp*0.54)
    zone2_up = round(ftp*0.74)
    zone3_up = round(ftp*0.89)
    zone4_up = round(ftp*1.04)
    zone5_up = round(ftp*1.2)
    zone6_up = round(ftp*1.49)
    ftp_table = {
        'FTP': ftp,
        '---': '---',
        '1 (<54%)': f'<{zone1_up}',
        '2 (55%-74%)': f'{zone1_up + 1}-{zone2_up}',
        '3 (75%-89%)': f'{zone2_up + 1}-{zone3_up}',
        '4 (90%-104%)': f'{zone3_up + 1}-{zone4_up}',
        '5 (105%-120%)': f'{zone4_up + 1}-{zone5_up}',
        '6 (121%-149%)': f'{zone5_up + 1}-{zone6_up}',
        '7 (>150%)': f'>{zone6_up + 1}',
    }

    return _as_table(ftp_table)


def _as_table(table):
    return [{'zone': k, 'power': v} for k, v in table.items()]
