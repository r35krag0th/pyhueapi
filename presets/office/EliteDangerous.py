#!/usr/bin/python
import os, sys
import json
from pprint import pprint

try:
    from iron_mq import *
except ImportError, ie:
    print "Please Install IronMQ Bindings for Python"
    print ""
    print "pip install iron-mq"
    print ""
    sys.exit(1)

class IronQueue:
    @staticmethod
    def get():
        project_token = '0NW3J3M4FljVVK2DoUzU5EwZIWk'
        project_id = '5681a0ce42887600090000dc'

        return IronMQ(
                host='mq-aws-eu-west-1-1.iron.io',
                project_id=project_id,
                token=project_token,
                protocol='https',
                port=443,
                api_version=3,
                config_file=None)

# If you're running from the app root this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))

# If you're running this from anywhere else this will make it work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset
from pyhueapi import hipchat_notification

if __name__ == '__main__':
    target_preset = Preset()

    # CT color mode
    # color_temperature = 340
    color_temperature = 340

    # Percentage
    front_lights_brightness = 30
    back_lights_brightness = 30

    # Parse any command-line arguments.
    target_preset.parse_arguments()

    # Define the preset
    preset_list = []
    for light_id in [2, 10, 12, 19, 20, 21, 22, 23, 24]:
        power_setting = None
        target_brightness = front_lights_brightness
        if light_id in [22]:
            # Top
            print "Building 22"
            power_setting = True
            target_brightness = 20

        elif light_id in [23]:
            print "Building 23"
            # Middle
            power_setting = True
            target_brightness = 30

        elif light_id in [24]:
            # Bottom
            print "Building 24"
            power_setting = True
            target_brightness = 30

        else:
            power_setting = True
            target_brightness = 10

        preset_list.append({'id': light_id, 'on': power_setting, 'bri': target_brightness, 'ct': color_temperature})

    pprint(preset_list)
    target_preset.define_preset(preset_list)
    hipchat_notification.send_preset('EliteDangerous', 'Office')
    target_preset.execute()

    broker = IronQueue.get()
    print "Queues: %s" % broker.queues()
    queue = broker.queue('lights-circadian')

    payload = {'room_id': 6, 'enabled':False}
    # queue.post(json.dumps(payload))
