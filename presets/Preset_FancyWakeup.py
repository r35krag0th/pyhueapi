#!/usr/bin/python

import PyHueAPI, os, sys
from time import sleep

if __name__ == '__main__':
    bottomFadeTime = 30
    middleFadeTime = 35
    topFadeTime = 40
    
    bottomFadeTime *= 10
    middleFadeTime *= 10
    topFadeTime *= 10
    
    preset1 = {
        1: {'on': True, 'bri': 254, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        2: {'on': True, 'bri': 254, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        3: {'on': True, 'bri': 253, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        
        4: {'on': True, 'bri': 236, 'xy': [0.674, 0.322], 'transitiontime': bottomFadeTime},
        5: {'on': True, 'bri': 236, 'xy': [0.674, 0.322], 'transitiontime': middleFadeTime},
        6: {'on': True, 'bri': 236, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
        
        8: {'on': True, 'bri': 236, 'xy': [0.674, 0.322], 'transitiontime': bottomFadeTime},
        9: {'on': True, 'bri': 236, 'xy': [0.674, 0.322], 'transitiontime': middleFadeTime},
        7: {'on': True, 'bri': 236, 'xy': [0.674, 0.322], 'transitiontime': topFadeTime},
                
        # Window Seat
        10: {'on': True, 'bri': 24, 'ct': 154, 'transitiontime': topFadeTime},
        
        # Cans
        11: {'on': True, 'bri': 24, 'ct': 154, 'transitiontime': topFadeTime},
        12: {'on': True, 'bri': 24, 'ct': 154, 'transitiontime': topFadeTime},
        13: {'on': True, 'bri': 24, 'ct': 154, 'transitiontime': topFadeTime},
        14: {'on': True, 'bri': 24, 'ct': 154, 'transitiontime': topFadeTime},
    }
    
    preset2 = {
        1: {'on': True, 'bri': 254, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        2: {'on': True, 'bri': 254, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        3: {'on': True, 'bri': 253, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        
        4: {'on': True, 'bri': 236, 'xy': [0.5576, 0.4074], 'transitiontime': bottomFadeTime},
        5: {'on': True, 'bri': 236, 'xy': [0.5576, 0.4074], 'transitiontime': middleFadeTime},
        6: {'on': True, 'bri': 236, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
        
        8: {'on': True, 'bri': 236, 'xy': [0.5576, 0.4074], 'transitiontime': bottomFadeTime},
        9: {'on': True, 'bri': 236, 'xy': [0.5576, 0.4074], 'transitiontime': middleFadeTime},
        7: {'on': True, 'bri': 236, 'xy': [0.5576, 0.4074], 'transitiontime': topFadeTime},
                
        # Window Seat
        10: {'on': True, 'bri': 24, 'ct': 154, 'transitiontime': topFadeTime},
        
        # Cans
        11: {'on': True, 'bri': 100, 'ct': 154, 'transitiontime': topFadeTime},
        12: {'on': True, 'bri': 100, 'ct': 154, 'transitiontime': topFadeTime},
        13: {'on': True, 'bri': 100, 'ct': 154, 'transitiontime': topFadeTime},
        14: {'on': True, 'bri': 100, 'ct': 154, 'transitiontime': topFadeTime},
    }
    
    
    preset3 = {
        1: {'on': True, 'bri': 254, 'ct': 362, 'transitiontime': topFadeTime},
        2: {'on': True, 'bri': 254, 'ct': 332, 'transitiontime': topFadeTime},
        3: {'on': True, 'bri': 253, 'ct': 303, 'transitiontime': topFadeTime},
        
        4: {'on': True, 'bri': 236, 'ct': 156, 'transitiontime': bottomFadeTime},
        5: {'on': True, 'bri': 236, 'ct': 156, 'transitiontime': middleFadeTime},
        6: {'on': True, 'bri': 236, 'ct': 156, 'transitiontime': topFadeTime},
        
        8: {'on': True, 'bri': 236, 'ct': 156, 'transitiontime': bottomFadeTime},
        9: {'on': True, 'bri': 236, 'ct': 156, 'transitiontime': middleFadeTime},
        7: {'on': True, 'bri': 236, 'ct': 156, 'transitiontime': topFadeTime},
                
        # Window Seat
        10: {'on': True, 'bri': 236, 'ct': 154, 'transitiontime': topFadeTime},
        
        # Cans
        11: {'on': True, 'bri': 236, 'ct': 154, 'transitiontime': topFadeTime},
        12: {'on': True, 'bri': 236, 'ct': 154, 'transitiontime': topFadeTime},
        13: {'on': True, 'bri': 236, 'ct': 154, 'transitiontime': topFadeTime},
        14: {'on': True, 'bri': 236, 'ct': 154, 'transitiontime': topFadeTime},
    }

    preset = [
        preset1,
        preset2,
        preset3
    ]

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)
    
    lights = PyHueAPI.Lights()
    for i in preset:
        print "Preset Started"
        for j in range(1,15):
            tmp = lights.get(j)
            data = i[j]
            
            if i == 1:
                data['transitiontime'] = 5
            tmp.bulkSetState(data)
            
        if i > 1:
            print "Sleeping..."
            sleep((topFadeTime / 10) + 1)