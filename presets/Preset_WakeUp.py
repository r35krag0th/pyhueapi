#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'bri': 254, 'ct': 362},
        3: {'on': True, 'bri': 253, 'ct': 303},
        2: {'on': True, 'bri': 254, 'ct': 332},
        5: {'on': True, 'bri': 236, 'ct': 156},
        4: {'on': True, 'bri': 236, 'ct': 156},
        7: {'on': True, 'bri': 236, 'ct': 156},
        6: {'on': True, 'bri': 236, 'ct': 156},
        9: {'on': True, 'bri': 236, 'ct': 156},
        8: {'on': True, 'bri': 236, 'ct': 156},
        10: {'on': False},
        11: {'on': False},
        12: {'on': False},
        13: {'on': False},
        14: {'on': False},
    }

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)

    lights = PyHueAPI.Lights()
    for i in range(1,15):
        tmp = lights.get(i)
        data = preset[i]

        tmp.bulkSetState(data)
