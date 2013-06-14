#!/usr/bin/python

import PyHueAPI, os, sys
from time import sleep
import numpy

if __name__ == '__main__':
    useLights = [
        1,2,3
    ]
    
    # In MINUTES
    fadeLength = 2
    timesPerMinute = (fadeLength * 60) - 10
    
    ### DRAGONS
    totalCycles = fadeLength * timesPerMinute
    napBetweenCycles = 60 / timesPerMinute
    
    # HUE
    minHue = 0
    maxHue = 65280
    currentHue = minHue
    
    delta = maxHue - minHue
    iDelta = delta / totalCycles
    
    lights = PyHueAPI.Lights()
    
    for poop in range(totalCycles):
        newHue = currentHue + iDelta
        print newHue
        
        for lightId in useLights:
            tmp = lights.get(lightId)
            tmp.setHue(newHue)
            tmp.setBrightness(255)
            sleep(0.02)
            
        currentHue = newHue
        sleep(napBetweenCycles)