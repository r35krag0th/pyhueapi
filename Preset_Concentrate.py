#!/usr/bin/python

import PyHueAPI

if __name__ == '__main__':
    preset = {
        1: {'on': True, 'bri': 255, 'ct': 233},
        3: {'on': True, 'bri': 255, 'ct': 233},
        2: {'on': True, 'bri': 255, 'ct': 233},
        5: {'on': True, 'bri': 255, 'ct': 233},
        4: {'on': True, 'bri': 255, 'ct': 233},
        7: {'on': True, 'bri': 255, 'ct': 233},
        6: {'on': True, 'bri': 255, 'ct': 233},
        9: {'on': True, 'bri': 255, 'ct': 233},
        8: {'on': True, 'bri': 255, 'ct': 233},
    }
    
    lights = PyHueAPI.Lights()
    for i in range(1,10):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)