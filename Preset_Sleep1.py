#!/usr/bin/python

import PyHueAPI

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        3: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        2: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        5: {'on': True, 'xy': [0.3196, 0.1852], 'bri': 145},
        4: {'on': True, 'xy': [0.2643, 0.1646], 'bri': 147},
        7: {'on': True, 'xy': [0.2432, 0.1903], 'bri': 157},
        6: {'on': True, 'xy': [0.2432, 0.1903], 'bri': 157},
        9: {'on': True, 'xy': [0.3196, 0.1852], 'bri': 145},
        8: {'on': True, 'xy': [0.2643, 0.1646], 'bri': 147},      
    }
    
    lights = PyHueAPI.Lights()
    for i in range(1,10):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)