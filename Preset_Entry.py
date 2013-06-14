#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'bri': 79, 'ct': 154},
        3: {'on': False, 'bri': 24, 'ct': 244},
        2: {'on': False, 'bri': 24, 'ct': 244},
        5: {'on': True, 'bri': 79, 'ct': 154},
        4: {'on': False, 'bri': 24, 'ct': 244},
        7: {'on': False, 'xy': [0.3767, 0.454], 'bri': 238},
        6: {'on': False, 'bri': 24, 'ct': 244},
        9: {'on': True, 'bri': 79, 'ct': 154},
        8: {'on': False, 'xy': [0.3943, 0.4887], 'bri': 238},
    }
    
    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)
    
    lights = PyHueAPI.Lights()
    for i in range(1,10):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)