import os

import setuptools

VERSION = '0.4.10'
DESCRIPTION = 'Strava Command-Line Tools'

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    python_requires='>=3.0',
    name='strava-cli',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=VERSION,
    author='Bartlomiej Wilczynski',
    author_email='me@bwilczynski.com',
    url='https://github.com/bwilczynski/strava-cli',
    packages=setuptools.find_packages(),
    install_requires=[
        'backports.zoneinfo==0.2.1',
        'certifi==2020.12.5',
        'chardet==3.0.4',
        'click==7.1.2',
        'click-option-group==0.5.2',
        'dateparser==1.0.0',
        'idna==2.8',
        'numpy==1.19.5',
        'oauthlib==3.1.0',
        'pandas==1.2.0',
        'python-dateutil==2.8.1',
        'pytz==2020.5',
        'regex==2020.11.13',
        'requests==2.22.0',
        'requests-oauthlib==1.3.0',
        'six==1.15.0',
        'strava-cli==0.4.10',
        'tabulate==0.8.7',
        'tzlocal==3.0b1',
        'urllib3==1.25.11',
    ],
    entry_points='''
        [console_scripts]
        strava=strava.cli.cli:cli
    ''',
    include_package_data=True,
)
