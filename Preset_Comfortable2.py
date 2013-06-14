#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'bri': 170, 'ct': 154},
        2: {'on': True, 'bri': 254, 'ct': 154},
        3: {'on': True, 'bri': 170, 'ct': 154},

        # Lamp W
        4: {'on': True, 'bri': 100, 'ct': 154},
        5: {'on': True, 'bri': 100, 'ct': 154},
        6: {'on': True, 'bri': 100, 'ct': 154},

        # Lamp E
        7: {'on': False, 'bri': 100, 'ct': 154},
        8: {'on': True,  'bri': 100, 'ct': 154},
        9: {'on': False, 'bri': 100, 'ct': 154},

        # Window Seat
        10: {'on': True, 'bri': 150, 'ct': 154},

        # Cans
        11: {'on': True,  'bri': 150, 'ct': 154},
        12: {'on': True,  'bri': 150, 'ct': 154},
        13: {'on': True,  'bri': 150, 'ct': 154},
        14: {'on': True,  'bri': 50, 'ct': 154},
    }

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)

    lights = PyHueAPI.Lights()
    for i in range(1,15):
        tmp = lights.get(i)
        data = preset[i]

        tmp.bulkSetState(data)
