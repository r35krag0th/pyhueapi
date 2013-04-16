#!/usr/bin/python

import PyHueAPI

if __name__ == '__main__':
    preset = {
        1: {'on': False},
        3: {'on': False},
        2: {'on': False},
        5: {'on': False},
        4: {'on': False},
        7: {'on': False},
        6: {'on': False},
        9: {'on': False},
        8: {'on': False},
    }
    
    lights = PyHueAPI.Lights()
    for i in range(1,10):
        tmp = lights.get(i)
        data = preset[i]
        
        tmp.bulkSetState(data)