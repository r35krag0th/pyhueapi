#!/usr/bin/python

import PyHueAPI
from time import sleep

if __name__ == '__main__':
    startPreset = {
        1: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        3: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        2: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        7: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        8: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        9: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},

        13: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        14: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},

        10: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},

        4: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        5: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        6: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        12: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},
        11: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 239},


    }
    
    endPreset = {
        1: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        3: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        2: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        5: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        4: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        7: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        6: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        9: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        8: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        10: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        11: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        12: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        13: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        14: {'on': True, 'xy': [0.6271, 0.3297], 'bri': 0},
        
    }
    
    deltas = {
        1: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        2: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        3: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        4: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        5: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        6: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        7: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        8: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        9: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        10: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        11: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        12: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        13: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
        14: {'x': 0, 'y': 0, 'xi': 0, 'yi': 0, 'b': 0, 'bi': 0},
    }
    
    currentValues = {
        1: [0, 0, 0],
        2: [0, 0, 0],
        3: [0, 0, 0],
        4: [0, 0, 0],
        5: [0, 0, 0],
        6: [0, 0, 0],
        7: [0, 0, 0],
        8: [0, 0, 0],
        9: [0, 0, 0],
        10: [0, 0, 0],
        11: [0, 0, 0],
        12: [0, 0, 0],
        13: [0, 0, 0],
        14: [0, 0, 0],        
    }
    
    # In MINUTES
    fadeLength = 30
    timesPerMinute = 4
    
    ### DRAGONS
    totalCycles = fadeLength * timesPerMinute
    napBetweenCycles = 60 / timesPerMinute
    
    lights = PyHueAPI.Lights()
    
    #print "Computing Deltas..."
    for i in range(1,15):
        """Compute all the deltas"""
        # Deltas
        deltas[i]['x'] = endPreset[i]['xy'][0] - startPreset[i]['xy'][0]
        deltas[i]['y'] = endPreset[i]['xy'][1] - startPreset[i]['xy'][1]
        deltas[i]['b'] = endPreset[i]['bri'] - startPreset[i]['bri']
        
        # Deltas per interval
        deltas[i]['xi'] = (deltas[i]['x'] / fadeLength) / timesPerMinute
        deltas[i]['yi'] = (deltas[i]['y'] / fadeLength) / timesPerMinute
        deltas[i]['bi'] = (deltas[i]['b'] / fadeLength) / timesPerMinute
        currentValues[i] = [
            startPreset[i]['xy'][0],
            startPreset[i]['xy'][1],
            startPreset[i]['bri']
            ]
        tmp = lights.get(i)
        tmp.bulkSetState({'xy': [currentValues[i][0], currentValues[i][1]], 'bri': currentValues[i][2]})
                
    #print deltas
    #print ""
    #print ""
        
    #print "Fading..."
    for i in range(1, totalCycles+1):
        sleep(napBetweenCycles)
        #print ""
        #print "Cycle %d of %d" % (i, totalCycles)
        
        for j in range(1,15):
            newX = currentValues[j][0] + deltas[j]['xi']
            newY = currentValues[j][1] + deltas[j]['yi']
            newB = currentValues[j][2] + deltas[j]['bi']
            
            #print "\tLight %d (x=%0.4f, y=%0.4f, b=%0.4f)" % (j, newX, newY, newB)
            currentValues[j][0] = newX
            currentValues[j][1] = newY
            currentValues[j][2] = newB
            
            tmp = lights.get(j)
            tmp.bulkSetState({'xy': [currentValues[j][0], currentValues[j][1]], 'bri': currentValues[j][2]})