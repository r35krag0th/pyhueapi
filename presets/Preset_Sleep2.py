#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        3: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        2: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        5: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        4: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        7: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        6: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        9: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        8: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        10: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        11: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        12: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        13: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
        14: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 238},
    }

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)

    lights = PyHueAPI.Lights()
    for i in range(1,15):
        tmp = lights.get(i)
        data = preset[i]

        tmp.bulkSetState(data)
