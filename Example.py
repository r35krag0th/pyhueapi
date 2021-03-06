#!/usr/local/bin/python

import pyhueapi
from pyhueapi.preset import Preset

if __name__ == '__main__':
    target_preset = Preset()
    
    # CT color mode
    color_temperature = 340
    
    # Percentage
    target_brightness_percent = 100
    
    # Parse any command-line arguments.
    target_preset.parse_arguments()
    
    # Define the preset
    target_preset.define_preset([
        {'id':  2, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
        {'id': 10, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
        {'id': 11, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
        {'id': 12, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
        {'id': 13, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
        {'id': 14, 'on': True, 'bri': target_brightness_percent, 'ct': color_temperature},
    ])
    
    target_preset.execute()