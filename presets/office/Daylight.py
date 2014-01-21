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
    color_temperature = 154

    # If we're overriding the default brightness here
    if len(sys.argv) > 1:
        target_brightness_percent = int(sys.argv[1])

    # Figure out what the actual brightness is from the percentage
    overall_brightness = PyHueAPI.compute_brightness_from_percentage(target_brightness_percent)

    # The preset map for changes to be made
    preset = {
        # Lamp E
        2: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},
        10: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},
        11: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},

        # Lamp W
        12: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},
        # 13: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},
        # 14: {'on': True, 'bri': overall_brightness, 'ct': color_temperature},
    }

    # Push the changes to all the lights
    PyHueAPI.make_changes(preset)
