#!/usr/bin/python

import PyHueAPI, os, sys
from time import sleep
import numpy

if __name__ == '__main__':
    waypoints = [
        (0.6750, 0.3220), # RED
        (0.1670, 0.0500), # BLUE
        (0.0700, 0.8000), # GREEN
        (0.3990, 0.5500), # YELLOW
        (0.5450, 0.4350)  # ORANGE
    ]
    
    useLights = [
        1,2,3,10,11,12,13,14
    ]
    
    # In MINUTES
    fadeLength = 1
    timesPerMinute = 58
    
    ### DRAGONS
    totalCycles = fadeLength * timesPerMinute
    napBetweenCycles = 60 / timesPerMinute
    
    ## Manage the cycles    
    numWaypoints = len(waypoints)
    currentWaypoint = (0, 0)
    lastWaypoint = (0, 0)
    nextWaypoint = (0, 0)
    
    lights = PyHueAPI.Lights()
    
    for waypointId in range(numWaypoints):
        lastWaypoint = currentWaypoint
        currentWaypoint = waypoints[waypointId]
        
        if waypointId + 1 < numWaypoints:
            nextWaypoint = waypoints[waypointId + 1]
        
        if waypointId == 0:
            print "FIRST"
            for lightId in useLights:
                tmp = lights.get(lightId)
                payload = {'xy': [currentWaypoint[0], currentWaypoint[1]], 'on': True, 'bri': 255}
                tmp.bulkSetState(payload)
        else:
            print "SUBSEQUENT"
            delta = numpy.subtract(currentWaypoint,lastWaypoint)

            print "-" * 80
            print "Current: ", currentWaypoint
            print "   Last: ", lastWaypoint
            print "   Next: ", nextWaypoint
            print "<<DELTA: (%4.4f, %4.4f)" % (delta[0], delta[1])
        
            print ""
            deltaPerInterval = numpy.divide(delta, (totalCycles))
            print " iDELTA: (%4.4f, %4.4f)" % (deltaPerInterval[0], deltaPerInterval[1])
            
            actualValue = lastWaypoint
            for i in range(totalCycles):
                actualValue = numpy.add(actualValue, deltaPerInterval)
                print " XY: (%4.4f, %4.4f)" % (actualValue[0], actualValue[1])
                
                for lightId in useLights:
                    tmp = lights.get(lightId)
                    payload = {'xy': [actualValue[0], actualValue[1]], 'on': True, 'bri': 255}
                    tmp.bulkSetState(payload)
                    sleep(0.02)
                sleep(napBetweenCycles)