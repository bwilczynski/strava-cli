import setuptools

VERSION = '0.4'

setuptools.setup(
    name='strava-cli',
    version=VERSION,
    author='Bartlomiej Wilczynski',
    author_email='me@bwilczynski.com',
    url='https://github.com/bwilczynski/strava-cli',
    packages=setuptools.find_packages(),
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
