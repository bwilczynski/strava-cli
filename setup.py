from setuptools import setup

VERSION = '0.1'

setup(
    name='strava-cli',
    version=VERSION,
    author='Bartlomiej Wilczynski',
    author_email='me@bwilczynski.com',
    url='https://github.com/bwilczynski/strava-cli',
    py_modules=['cli'],
    install_requires=[
        'click',
        'requests',
        'requests_oauthlib',
        'tabulate'
    ],
    entry_points='''
        [console_scripts]
        strava=cli:cli
    ''',
)
