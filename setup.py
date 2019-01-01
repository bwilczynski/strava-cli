import setuptools

VERSION = '0.2'

setuptools.setup(
    name='strava-cli',
    version=VERSION,
    author='Bartlomiej Wilczynski',
    author_email='me@bwilczynski.com',
    url='https://github.com/bwilczynski/strava-cli',
    packages=[
        'strava'
    ],
    install_requires=[
        'click',
        'requests',
        'requests_oauthlib',
        'tabulate',
        'dateparser'
    ],
    entry_points='''
        [console_scripts]
        strava=strava.cli:cli
    ''',
)
