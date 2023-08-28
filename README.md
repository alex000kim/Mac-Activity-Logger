# Mac Activity Logger

This script logs the currently active application and related metadata to a local SQLite database on macOS.
The goal of the project is to help me understand how I spend my time on my computer.
Some ways how this data could be used later:

- Generate reports showing the amount of time spent in each application. Identify trends in usage over time.
- Analyze time spent on websites and categorize them as productive, leisure, educational, etc.
- Set goals for certain metrics, like maximum hours per day spent on leisure websites. Track progress towards these goals over time.
- Use URL data to identify patterns.
- Apply machine learning to app and website categories to automatically detect productive vs distracting usage patterns.

## Features

- Logs the foreground application name every time the script is run
- If Google Chrome is the active app, also logs the active tab URL and title
- Saves timestamped records to a SQLite database for persistent storage
- Uses AppKit via AppleScript to get active app information
- Errors are logged to a separate file for diagnostics

## Requirements

- macOS
- Python 3
- SQLite 3

## Usage

- Run the `mac_activity_logger.py` script on a schedule via Launchpad or cron
- The local SQLite database will be created at `~/Documents/app_activity_db.sqlite`
- Log files will be created at `~/Documents/app_activity_errors.log`
- View and query the database with SQLite tools like DB Browser for SQLite

## Run on Startup

To run this script in the background on startup every 5 seconds, you can create a launchd plist file.

Here are the steps:

1. Create a file `~/Library/LaunchAgents/com.user.app_activity.plist` with this content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.user.app_activity</string>

  <key>ProgramArguments</key>
  <array>
    <string>python</string>
    <string>/full/path/to/your_script.py</string>
  </array>

  <key>StartInterval</key>
  <integer>5</integer>
  
  <key>RunAtLoad</key>
  <true/>
  
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
```

2. Load the plist to start the script:

```bash
launchctl load ~/Library/LaunchAgents/com.user.app_activity.plist
```
