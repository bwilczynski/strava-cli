import click
import datetime

@click.command(name='cw',
               help='Helper to get the current calendar week')
def get_cw():
    click.echo(datetime.datetime.now().isocalendar()[1])
