#!/usr/bin/python

import PyHueAPI, os, sys
from time import sleep

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