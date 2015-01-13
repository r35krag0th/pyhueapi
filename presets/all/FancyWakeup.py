#!/usr/bin/python
import os, sys

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset
from time import sleep
from pyhueapi import irc_notification

if __name__ == '__main__':
    bottomFadeTime = 30
    middleFadeTime = 35
    topFadeTime = 40

    bottomFadeTime *= 1000
    middleFadeTime *= 1000
    topFadeTime *= 1000

    preset0 = []
    for i in range(1,18):
        preset0.append({'id': i, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': 0})

    preset1 = [
        {'id': 1, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 3, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},

        {'id': 4, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': bottomFadeTime},
        {'id': 5, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': middleFadeTime},
        {'id': 6, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},

        {'id': 8, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': bottomFadeTime},
        {'id': 9, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': middleFadeTime},
        {'id': 7, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},

        {'id': 2,  'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 10, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 12, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},

        {'id': 11, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 13, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 14, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},

        {'id': 15, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 16, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        {'id': 17, 'on': True, 'bri': 10, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
    ]

    preset2 = [
        {'id': 1, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 2, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 3, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},

        {'id': 4, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': bottomFadeTime},
        {'id': 5, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': middleFadeTime},
        {'id': 6, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},

        {'id': 7, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 8, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': bottomFadeTime},
        {'id': 9, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': middleFadeTime},

        {'id': 10, 'on': True, 'bri': 10, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},

        {'id': 11, 'on': True, 'bri': 50, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 12, 'on': True, 'bri': 50, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 13, 'on': True, 'bri': 50, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 14, 'on': True, 'bri': 50, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},

        {'id': 15, 'on': True, 'bri': 50, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 16, 'on': True, 'bri': 50, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        {'id': 17, 'on': True, 'bri': 100, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
    ]


    preset3 = [
        # Master N/S
        {'id': 1,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': topFadeTime},
        {'id': 3,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': topFadeTime},

        # Master Lamp 1
        {'id': 4,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': bottomFadeTime},
        {'id': 5,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': middleFadeTime},
        {'id': 6,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': topFadeTime},

        # Master Lamp 2
        {'id': 8,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': bottomFadeTime},
        {'id': 9,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': middleFadeTime},
        {'id': 7,  'on': True, 'bri': 100, 'ct': 156, 'transitiontime': topFadeTime},

        # Living Room Lamp
        {'id': 2,  'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},
        {'id': 10, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},
        {'id': 12, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},

        # Living Room Single Lamps
        {'id': 11, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},
        {'id': 13, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},
        {'id': 14, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},

        # Dining Room Lights
        {'id': 15, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},
        {'id': 16, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},

        # Coffee Table
        {'id': 16, 'on': True, 'bri': 100, 'ct': 340, 'transitiontime': topFadeTime},
    ]

    preset = [
        preset1,
        preset2,
        preset3
    ]

    target_preset = Preset()

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    #
    target_preset.define_preset(preset0)

    irc_notification.send_preset('Fancy Wakeup', 'all')
    target_preset.execute()

    # from pprint import pprint
    for i in preset:
        # pprint(i)
        # print "------------------------------------------"
        target_preset.define_preset(i)
        target_preset.execute()

        if i > 1:
            print "Sleeping..."
            # sleep((topFadeTime / 10) + 1)
            sleep(45)
            # sleep(2)
