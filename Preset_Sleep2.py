#!/usr/bin/python

import PyHueAPI

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
    }
    
    lights = PyHueAPI.Lights()
    for i in range(1,10):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)