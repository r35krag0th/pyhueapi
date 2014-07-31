#!/usr/bin/python
import os, sys

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset

if __name__ == '__main__':
    target_preset = Preset()

    # CT color mode
    color_temperature = 340

    # Percentage
    target_brightness_percent = 80

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    # Define the preset
    first_color = [0.408, 0.517]
    second_color = [0.168, 0.041]

    target_preset.define_preset([
        # {'id':  2, 'on': True, 'bri': target_brightness_percent, 'xy': first_color},
        # {'id': 10, 'on': True, 'bri': target_brightness_percent, 'xy': first_color},
        # {'id': 12, 'on': True, 'bri': target_brightness_percent, 'xy': first_color},
        {'id': 13, 'on': True, 'bri': target_brightness_percent, 'xy': second_color},
        {'id': 14, 'on': True, 'bri': target_brightness_percent, 'xy': second_color},
        {'id': 15, 'on': True, 'bri': target_brightness_percent, 'xy': second_color},
        {'id': 16, 'on': True, 'bri': target_brightness_percent, 'xy': second_color},
    ])

    target_preset.execute()
