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

    # X,Y Color Mode
    color_temperature = 154

    # Percentage
    target_brightness_percent = 100

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    # Define the preset
    final_preset = []
    # for light_id in [1, 3, 4, 5, 6, 7, 8, 9]:
    for light_id in [2, 10, 12]:
        final_preset.append({
            'id': light_id,
            'on': False,
            'bri': target_brightness_percent,
            'ct': color_temperature,
        })
    target_preset.define_preset(final_preset)

    hipchat_notification.send_preset('Off', 'Office')
    target_preset.execute()
