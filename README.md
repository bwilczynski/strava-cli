# Strava command-line interface

[![Build Status](https://dev.azure.com/bwilczyn/strava-cli/_apis/build/status/bwilczynski.strava-cli?branchName=master)](https://dev.azure.com/bwilczyn/strava-cli/_build/latest?definitionId=1&branchName=master)

Uses [Strava API](https://developers.strava.com/docs/reference/) to access Strava dataset.

## Installation

Using `Homebrew` on OSX:

```sh
brew tap bwilczynski/tap
brew install strava-cli
```

Using `pip` (requires Python 3):

```sh
pip install strava-cli
```

## Usage

```sh
strava [OPTIONS] COMMAND [ARGS]
```

### Get Started

[Create application](https://www.strava.com/settings/api) and run `strava config` to provide 
your application's Client ID and Client Secret.

Alternatively set the following environment variables before running `strava`:

```sh
export STRAVA_CLIENT_ID={YOUR_CLIENT_ID}
export STRAVA_CLIENT_SECRET={YOUR_CLIENT_SECRET}
```

Login to your Strava service (opens a web browser sending user to Strava login service):

```sh
strava login
```

For usage and help content, pass in the `--help` parameter, for example:

```sh
strava --help
```

### Available commands

Get recent, yearly, total stats:

```console
➜ strava stats  

Type        Count  Distance    Moving time    Elevation gain
--------  -------  ----------  -------------  ----------------
🏃 recent        7  53.33 km    5h 6m          166 m
🏃 ytd         121  1048.15 km  95h 43m        4526 m
🏃 all         241  1761.13 km  164h 35m       7258 m

```

Get last 5 activities:

```console
➜ strava activities -pp 5

        Id  Start date                 Name             Elapsed time    Distance    Average speed
----------  -------------------------  ---------------  --------------  ----------  ---------------
2038696223  2018-12-27 17:58:49+01:00  🏃 Afternoon Run  45:19           8.02 km     05:15 /km
2034884699  2018-12-25 15:38:55+01:00  🏃 Bday Run       44:56           7.32 km     05:41 /km
2031636166  2018-12-23 14:29:50+01:00  🏃 Afternoon Run  48:14           6.55 km     06:17 /km
2030237887  2018-12-22 20:13:31+01:00  🏃 Evening Run    37:34           7.10 km     05:16 /km
2020398424  2018-12-16 16:39:56+01:00  🏃 Afternoon Run  41:54           6.31 km     05:43 /km
```

Get activities after / before a certain date:

```sh
strava activities --after="2 weeks ago" --before="1 week ago"
```

```sh
strava activities --after="2018-12-01"
```

Get detailed activity information:

```console
➜ strava activity 1958241710

Name:                  🏃 30. Bieg Niepodległości
Description:           Oficjalny czas: 46:55
Start date:            2018-11-11 11:24:28+01:00
Elapsed time:          46:58
Distance:              10.02 km
Average speed:         04:41 /km
Total elevation gain:  52 m
Calories:              639.0
Device name:           Garmin Forerunner 645 Music
Gear:                  New Balance Zante v4 (443.65 km)
Split 1:               👟 04:44 /km ❤ 164 bpm ⬆ 7 m
Split 2:               👟 04:38 /km ❤ 168 bpm ➡ 0 m
Split 3:               👟 04:48 /km ❤ 164 bpm ⬆ 1 m
Split 4:               👟 04:49 /km ❤ 160 bpm ⬇ -3 m
Split 5:               👟 04:41 /km ❤ 161 bpm ⬇ -2 m
Split 6:               👟 04:37 /km ❤ 164 bpm ⬆ 2 m
Split 7:               👟 04:50 /km ❤ 165 bpm ⬆ 3 m
Split 8:               👟 04:39 /km ❤ 163 bpm ⬇ -1 m
Split 9:               👟 04:42 /km ❤ 165 bpm ➡ 0 m
Split 10:              👟 04:24 /km ❤ 171 bpm ⬇ -9 m
Split 11:              👟 04:44 /km ❤ 173 bpm ⬇ -1 m

```
Or use `xargs`:

```sh
strava activities -q --after="1 day ago" | xargs strava activity 
```

Combine JSON output with `jq`:

```console
➜ strava activities -pp 1 -q | xargs strava activity --output json | jq ".name"
"Afternoon Run"
```

Upload Activity from GPX (example: export from a competing service):
```sh
strava upload ./2020-09-27-145141.gpx
```
```console
Id:      4717164254
Status:  Your activity is still being processed.
Error:   None
```

Can upload multiple activities.
```sh
strava upload ./*.gpx
```
