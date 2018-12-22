# Strava command-line interface

Uses [Strava API](https://developers.strava.com/docs/reference/) to access Strava dataset.

## Usage

```bash
$ strava [OPTIONS] COMMAND [ARGS]
```

### Get Started

[Create application](https://www.strava.com/settings/api) and set the following environment variables before running `strava`:

```bash
export STRAVA_CLIENT_ID={YOUR_CLIENT_ID}
export STRAVA_CLIENT_SECRET={YOUR_CLIENT_SECRET}
```

Login to your Strava service (opens a web browser sending user to Strava login service):

```bash
$ strava login
```

For usage and help content, pass in the `--help` parameter, for example:

```bash
$ strava --help
```

### Available commands

TBD