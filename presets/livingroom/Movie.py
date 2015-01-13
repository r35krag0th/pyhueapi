#!/usr/bin/python
import os, sys

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset
from pyhueapi import irc_notification

if __name__ == '__main__':
    target_preset = Preset()

    # CT color mode
    color_temperature = 340
    # xy_color = [0.139, 0.081]   # Blue
    xy_color = [0.3133, 0.3289] # White

    # Percentage
    target_brightness_percent = 10

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    # Define the preset
    target_preset.define_preset([
        # {'id':  2, 'on': False, 'bri': target_brightness_percent, 'ct': color_temperature},    # Triple Lamp
        # {'id': 10, 'on': False, 'bri': target_brightness_percent, 'ct': color_temperature},    # Triple Lamp
        # {'id': 12, 'on': False, 'bri': target_brightness_percent, 'ct': color_temperature},    # Triple Lamp

        {'id': 13, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},    # Living Room (North Couch)
        {'id': 14, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},    # Living Room (South Couch)

        {'id': 15, 'on': False, 'bri': target_brightness_percent, 'ct': color_temperature},     # Dining (Niche)
        {'id': 16, 'on': False, 'bri': target_brightness_percent, 'ct': color_temperature},    # Dining (Table)
        {'id': 17, 'on': True,  'bri': 100, 'xy': xy_color},             # Living Room (Couch Backlight)
    ])

    irc_notification.send_preset('Movie', 'Living Room')

    target_preset.execute()
