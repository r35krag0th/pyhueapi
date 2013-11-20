#!/usr/bin/python

import PyHueAPI, os, sys

if __name__ == '__main__':
    overall_brightness = 80
    color_temperature = 154

    preset = {
        1: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},
        3: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},

        # Lamp W
        5: {'on': False, 'bri': overall_brightness, 'ct': color_temperature},
        4: {'on': False, 'bri': overall_brightness, 'ct': color_temperature},
        6: {'on': False, 'bri': overall_brightness, 'ct': color_temperature},

        # Lamp E
        8: {'on': False, 'bri': overall_brightness, 'ct': color_temperature},
        7: {'on': False, 'bri': overall_brightness, 'ct': color_temperature},
        9: {'on': False, 'bri': overall_brightness, 'ct': color_temperature},
    }

    # TRAP
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)

    lights = PyHueAPI.Lights()
    for i in preset.keys():
        tmp = lights.get(i)
        data = preset[i]

        tmp.bulkSetState(data)
