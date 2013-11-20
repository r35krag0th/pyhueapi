#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'bri': 24, 'ct': 154},
        3: {'on': True, 'bri': 24, 'ct': 154},
        2: {'on': True, 'bri': 24, 'ct': 154},
        5: {'on': True, 'bri': 24, 'ct': 154},
        4: {'on': True, 'bri': 24, 'ct': 154},
        7: {'on': False, 'xy': [0.3767, 0.454], 'bri': 238},
        6: {'on': True, 'bri': 24, 'ct': 154},
        9: {'on': False, 'xy': [0.3521, 0.4054], 'bri': 238},
        8: {'on': False, 'xy': [0.3943, 0.4887], 'bri': 238},
        10: {'on': False},
        11: {'on': False},
        12: {'on': False, 'bri': 24, 'ct': 154},
        13: {'on': True, 'bri': 24, 'ct': 154},
        14: {'on': False},
    }

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)
    
    lights = PyHueAPI.Lights()
    for i in range(1,15):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)