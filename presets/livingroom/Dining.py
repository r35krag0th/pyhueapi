#!/usr/bin/python
import os, sys

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset
from pyhueapi import hipchat_notification

if __name__ == '__main__':
    target_preset = Preset()

    # CT color mode
    color_temperature = 340

    # Percentage
    target_brightness_percent = 75

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    # Define the preset
    target_preset.define_preset([
        {'id': 15, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
        {'id': 16, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
    ])

    hipchat_notification.send_preset('Dining On', 'Living Room')

    target_preset.execute()
