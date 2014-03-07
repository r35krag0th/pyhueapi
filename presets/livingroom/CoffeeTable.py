#!/usr/bin/python
import os, sys, random

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset

if __name__ == '__main__':
    target_preset = Preset()

    # CT color mode
    color_temperature = 340

    # Percentage
    target_brightness_percent = 80

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    # [0.4369, 0.1879] to [0.4173, 0.5373]
    # Define the preset
    first_color =  [0.4369, 0.1879]  # ORANGE
    second_color = [0.4369, 0.5373]   # BLUE

    y_lower_limit = 0.1879
    y_upper_limit = 0.5373

    color_choices = {}
    color_choices['red'] = [0.703, 0.296]
    color_choices['magenta'] = [0.3681, 0.1683]
    color_choices['purple'] = [0.2977, 0.1415]
    color_choices['blue'] = [0.1393,0.0813]
    color_choices['cyan'] = [0.1605,0.311]
    color_choices['green'] = [0.214,0.709]
    color_choices['yellow'] = [0.426,0.5299]
    color_choices['orange'] = [0.6222,0.3642]

    color_names = color_choices.keys()
    number_of_choices = len(color_names) - 1

    picked_index = random.randint(0, number_of_choices)
    # print "Picked Index: %d" % picked_index
    # print "Color Name: %s" % color_names[picked_index]
    preset_color_value = color_choices[color_names[picked_index]]

    target_preset.define_preset([
        {'id': 17, 'on': True, 'bri': target_brightness_percent, 'xy': preset_color_value, 'transitiontime': 300}, # 30 seconds
    ])

    target_preset.execute()
