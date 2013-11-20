#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'bri': 255, 'ct': 233, 'colormode': 'ct'},
        2: {'on': True, 'bri': 255, 'ct': 233, 'colormode': 'ct'},
        3: {'on': True, 'bri': 255, 'ct': 233, 'colormode': 'ct'},
        
        ## LAMP
        4: {'on': True, 'bri': 250, 'ct': 233, 'colormode': 'ct'},
        5: {'on': True, 'bri': 250, 'ct': 233, 'colormode': 'ct'},
        6: {'on': True, 'bri': 250, 'ct': 233, 'colormode': 'ct'},
        
        ## LAMP
        7: {'on': True, 'bri': 250, 'ct': 233, 'colormode': 'ct'},
        8: {'on': True, 'bri': 250, 'ct': 233, 'colormode': 'ct'},
        9: {'on': True, 'bri': 250, 'ct': 233, 'colormode': 'ct'},
        
        ## Ceiling
        10: {'on': False, 'bri': 25, 'ct': 233, 'colormode': 'ct'},
        11: {'on': False, 'bri': 25, 'ct': 233, 'colormode': 'ct'},
        12: {'on': False, 'bri': 25, 'ct': 233, 'colormode': 'ct'},
        13: {'on': False, 'bri': 25, 'ct': 233, 'colormode': 'ct'},
        14: {'on': False, 'bri': 25, 'ct': 233, 'colormode': 'ct'},
    }

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)

    lights = PyHueAPI.Lights()
    for i in range(1,15):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)