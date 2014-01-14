#!/usr/bin/env python

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
    color_temperature = 154

    # If we're overriding the default brightness here
    if len(sys.argv) > 1:
        target_brightness_percent = int(sys.argv[1])

    # Figure out what the actual brightness is from the percentage
    overall_brightness = PyHueAPI.compute_brightness_from_percentage(target_brightness_percent)

    # The preset map for changes to be made
    preset = {
        1: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        2: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        3: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        4: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        5: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        6: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        7: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        8: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        9: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        10: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        11: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        12: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        13: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
        14: {'on': True, 'xy': [0.2404, 0.0816], 'bri': 254},
    }

    # Push the changes to all the lights
    PyHueAPI.make_changes(preset)
