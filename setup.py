import os

import setuptools

VERSION = "0.7.0"
DESCRIPTION = "Strava Command-Line Tools"

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    python_requires=">=3.0",
    name="strava-cli",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=VERSION,
    author="Bartlomiej Wilczynski",
    author_email="me@bwilczynski.com",
    url="https://github.com/bwilczynski/strava-cli",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "requests",
        "requests_oauthlib",
        "tabulate",
        "dateparser",
    ],
    entry_points="""
        [console_scripts]
        strava=strava.cli:cli
    """,
    include_package_data=True,
)
