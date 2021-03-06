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
    xy_color = [0.2404, 0.0816]

    # Percentage
    target_brightness_percent = 100

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    white_color = 155;
    yellow_color = 337;

    # Define the preset
    final_preset = [
            {'id': 1,  'on': True, 'bri': 25, 'ct': white_color, 'transitiontime': 10000 },
            {'id': 3,  'on': True, 'bri': 25, 'ct': white_color, 'transitiontime': 10000 },
            {'id': 11, 'on': True, 'bri': 85, 'ct': white_color, 'transitiontime': 10000 },

            {'id': 2,  'on': True, 'bri': 25, 'ct': yellow_color, 'transitiontime': 10000 },
            {'id': 10, 'on': True, 'bri': 25, 'ct': yellow_color, 'transitiontime': 10000 },
            {'id': 12, 'on': True, 'bri': 25, 'ct': yellow_color, 'transitiontime': 10000 },
            {'id': 17, 'on': True, 'bri': 100, 'xy': [0.3682, 0.1633], 'transitiontime': 10000 },

            {'id':  4, 'on': False, 'bri': 50, 'ct': white_color},
            {'id':  5, 'on': False, 'bri': 50, 'ct': white_color},
            {'id':  6, 'on': False, 'bri': 50, 'ct': white_color},
            {'id':  7, 'on': False, 'bri': 50, 'ct': white_color},
            {'id':  8, 'on': False, 'bri': 50, 'ct': white_color},
            {'id':  9, 'on': False, 'bri': 50, 'ct': white_color},
            {'id': 13, 'on': False, 'bri': 50, 'ct': white_color},
            {'id': 14, 'on': False, 'bri': 50, 'ct': white_color},
            {'id': 15, 'on': False, 'bri': 50, 'ct': white_color},
            {'id': 16, 'on': False, 'bri': 50, 'ct': white_color},
            ]
    target_preset.define_preset(final_preset)

    hipchat_notification.send_preset('Entry', 'all')
    target_preset.execute()
