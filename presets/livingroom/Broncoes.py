#!/usr/bin/python

# Usual "stuff" needed
import os, sys

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

# Import the PyHueAPI Library
import PyHueAPI

if __name__ == '__main__':
    # By default use 80% brightness
    target_brightness_percent = 80

    # Target color temperature; 154 is a nice daylight color
    color_temperature = 340

    # If we're overriding the default brightness here
    if len(sys.argv) > 1:
        target_brightness_percent = int(sys.argv[1])

    # Figure out what the actual brightness is from the percentage
    overall_brightness = PyHueAPI.compute_brightness_from_percentage(target_brightness_percent)

    # The preset map for changes to be made
    a = [0.5489, 0.4137]
    preset = {
        11: {'on': True, 'bri': overall_brightness, 'xy': a},
        13: {'on': True, 'bri': overall_brightness, 'xy': a},
        14: {'on': True, 'bri': overall_brightness, 'xy': a},
    }

    # Push the changes to all the lights
    PyHueAPI.make_changes(preset)

    b = [0.168, 0.041]
    preset = {
        2: {'on': True, 'bri': overall_brightness,  'xy': b},
        10: {'on': True, 'bri': overall_brightness, 'xy': b},
        12: {'on': True, 'bri': overall_brightness, 'xy': b},
    }
    PyHueAPI.make_changes(preset)
