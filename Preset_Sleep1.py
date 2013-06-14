#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        # RED
        1: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        3: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        2: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        7: {'on': True, 'xy': [0.2432, 0.1903], 'bri': 157},
        8: {'on': True, 'xy': [0.2643, 0.1646], 'bri': 147},
        9: {'on': True, 'xy': [0.3196, 0.1852], 'bri': 145},

        13: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        14: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},

        10: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        
        # BLUE
        4: {'on': True, 'xy': [0.2643, 0.1646], 'bri': 147},
        5: {'on': True, 'xy': [0.3196, 0.1852], 'bri': 145},
        6: {'on': True, 'xy': [0.2432, 0.1903], 'bri': 157},
        
        12: {'on': True, 'xy': [0.2643, 0.1646], 'bri': 147},
        11: {'on': True, 'xy': [0.3196, 0.1852], 'bri': 145},
    }
    
    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)
    
    lights = PyHueAPI.Lights()
    for i in range(1,15):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)