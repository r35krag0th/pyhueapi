#!/usr/bin/python

from __future__ import division

import os, sys
import requests, json
import time
from time import sleep
from datetime import datetime
import math
from threading import Thread

import traceback

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

# This is mostly going to use the HTTP API for speed
# https://lights.r35.private/api.php?
#   light_group_id = %s
#   color_temperature = %s

# Sunrise and Sunset information are already gathered by tools at
# https://hud.r35.private/sunrise.php

def simple_log(something_to_log):
    print "[%s] %s" % (datetime.now().strftime("%m-%d-%Y %H:%I:%S"), something_to_log)

def build_hour_range(first_hour, last_hour):
    return range(first_hour, last_hour + 1)

class CircadianHue:
    running = False

    sunrise = None
    sunset = None
    midday = None

    def __init__(self):
        simple_log("CircadianHue Loading...")
        self.get_sunrise_and_sunset()
        self.running = True

    def get_sunrise_and_sunset(self):
        # print "Fetching Sunrise and Sunset information"
        response = requests.get("https://hud.r35.private/sunrise.php", verify=False)
        data = response.json()

        self.sunrise = data['sunrise']['epoch']
        self.sunset = data['sunset']['epoch']
        self.midday = self.sunrise + ((self.sunset - self.sunrise) / 2)

    def determine_color_temperature(self):
        # print "Determining the color temperature for the current time of day"

        now = time.time()
        initial_color = 2700

        if now < self.sunrise:
            initial_color = 2700
        elif now > self.sunset:
            initial_color = 2700
        else:
            if now < self.midday:
                initial_color = 2700 + ((now - self.sunrise) / (self.midday - self.sunrise) * 3300)
            else:
                initial_color = 6000 - ((now - self.midday) / (self.sunset - self.midday) * 3300)

        # Make sure we floor, then hack off the extra precision
        return int(math.floor(initial_color))

    def kelvin_to_mired(self, temp_k):
        return 1000000 / temp_k

    def mired_to_kelvin(self, temp_m):
        return 1000000 / temp_m

    def brightness_from_percent(self, a_brightness):
        # print "brightness_from_percent(%d)" % a_brightness
        result = (a_brightness / 100) * 255
        # print " ====> %d" % result
        return result

    def percent_from_brightness(self, a_brightness):
        # print "percent_from_brightness(%d)" % a_brightness
        result = a_brightness / 255
        # print " ====> %d" % result
        return a_brightness / 255


    def compute_desired_brightness(self):
        now = time.time()
        current_hour = datetime.now().hour

        # between 12:00AM and 05:59AM (5%  ) x
        # between 06:00AM and 08:59AM (15% ) x
        # between 09:00AM and SUNSET  (100%) xxxx
        # between SUNSET  and 08:00PM (75% ) xxx
        # between 08:00PM and 09:59PM (50% ) xx
        # between 10:00PM and 12:00AM (25% ) x

        # Stages
        #   + Should be asleep    [00:00 - 06:00]
        #   + Should be waking up [06:00 - 09:00]
        #   + Normal              [09:00 - SUNSET]
        #   + Early Evening       [SUNSET - 20:00]
        #   + Late Evng Phase 1   [21:00 - 21:00]
        #   + Late Evng Phase 2   [21:00

        print "SunRise => %s" % self.sunrise
        print "SunSet  => %s" % self.sunset

        # Auto-compute this?
        if current_hour == 22 or current_hour == 23:
            return 15
        elif current_hour >= 0 and current_hour < 6:
            return 5
        elif current_hour >= 6 and current_hour <= 8:
            return 100
        elif current_hour >= 9 and now < self.sunset:
            return 95
        elif now >= self.sunset and current_hour < 20:
            return 50
        elif current_hour == 21:
            return 25
        else:
            return None

    def do_lighting_update(self, light_group, color_temp):
        # Probably could simply this into less calls
        response = requests.get("https://lights.r35.net/api.php?light_group_id=%d" % light_group, verify=False)
        check_data = response.json()

        human_group_name = 'Unknown'
        if light_group == 6: human_group_name = 'Master Bedroom: All'
        if light_group == 2: human_group_name = 'Office: All'

        print check_data

        if not check_data['action']['on'] == True:
            simple_log("\033[34mLightGroup(%d)[%s] is not on.\033[0m" % (light_group, human_group_name))
            return

        if check_data['action']['ct'] == color_temp:
            simple_log("LightGroup(%d)[%s] is already set to %d Mired (%dK)" % (light_group, human_group_name, color_temp, self.mired_to_kelvin(color_temp)))
            return
        else:
            simple_log("~~ LightGroup(%d)[%s] Current_CT=%d, Desired_CT=%d" % (light_group, human_group_name, check_data['action']['ct'], color_temp))

        desired_brightness = self.compute_desired_brightness()

        # Made it past the checks; now do the work
        simple_log("\033[32mSetting LightGroup(%d)[%s] to %d Mired (%dK)\033[0m" % (light_group, human_group_name, color_temp, self.mired_to_kelvin(color_temp)))

        # Parameters
        light_params = {'light_group_id': light_group, 'rawct': color_temp}

        if not None == desired_brightness and not check_data['action']['bri'] == desired_brightness:
            simple_log("\t>>> Changing brightness as well ==> %d" % desired_brightness)
            light_params['brightness'] = int(desired_brightness)

        response = requests.get("https://lights.r35.net/api.php", verify=False, params=light_params)

        if not response.status_code == 200:
            simple_log("\t>>> Failed: %s", response.json())

    ## We could cache these methods, BUT they're already pretty cached anyways.
    def is_group_on(self, light_group_id):
        response = requests.get("https://lights.r35.net/api.php?light_group_id=%d" % light_group_id, verify=False)
        data = response.json()

        return data['action']['on']


    def get_current_ct(self, light_group_id):
        response = requests.get("https://lights.r35.net/api.php?light_group_id=%d" % light_group_id, verify=False)
        return response.json()['action']['ct']

    def update_rooms(self, room_list):
        for room_id in room_list:
            simple_log("\033[1;32mUpdating Room\033[0m(%d:%s)" % (room_id, room_names.get(room_id, room_id)))
            self.do_lighting_update(room_id, self.kelvin_to_mired(app.determine_color_temperature()))


if __name__ == '__main__':
    simple_log("Main App starting")
    app = CircadianHue()

    # 1 = MBR(Nightstand Lamps)
    # 2 = Office(All)
    # 3 = Living Room
    # 4 = Dining
    # 5 = MBR(Floor Lamps)
    # 6 = MBR(All)

    enabled_rooms = [2, 6]
    disabled_rooms = [1, 3, 4, 5]

    broker = IronQueue.get()
    print "Queues: %s" % broker.queues()
    queue = broker.queue('lights-circadian')

    # How often we're going to change the lighting (seconds)
    refresh_interval = 300
    last_refresh = 0

    room_names = {
            1: 'Master Bedroom: Nightstand',
            2: 'Office: All',
            3: 'Living Room: All',
            4: 'Dining Room: All',
            5: 'Master Bedroom: Floor',
            6: 'Master Bedroom: All',
            }

    room_state_changed = False

    while app.running:
        room_state_changed = False
        try:
            queue_data = queue.reserve(max=10, timeout=None, wait=30, delete=True)
            if len(queue_data['messages']) > 0:
                print "\033[1;35m[Queue Data]\033[0m %s" % queue_data
            for message in queue_data['messages']:
                json_data = json.loads(message['body'])
                # print "From Queue: %s" % message
                # print "\033[1;35mFrom Queue[JSON]:\033[0m %s" % json_data

                room_id = json_data.get('room_id', None)
                is_enabled = json_data.get('enabled', None)

                if not room_id == None and not is_enabled == None:
                    if not room_id in enabled_rooms and is_enabled == True:
                        enabled_rooms.append(room_id)
                        disabled_rooms.remove(room_id)
                        room_state_changed = True

                        # Update the room now that it's enabled
                        app.update_rooms([room_id])

                    if room_id in enabled_rooms and is_enabled == False:
                        enabled_rooms.remove(room_id)
                        disabled_rooms.append(room_id)
                        room_state_changed = True

            now = time.time()
            refresh_delta = now - last_refresh

            if refresh_delta > refresh_interval:
                simple_log("It's been over %ds (~%ds), updating lights..." % (refresh_interval, refresh_delta))
                # app.get_sunrise_and_sunset()

                app.update_rooms(enabled_rooms)
                # for room_id in enabled_rooms:
                #     simple_log("\033[1;32mUpdating Room\033[0m(%d:%s)" % (room_id, room_names.get(room_id, room_id)))
                #     app.do_lighting_update(room_id, app.kelvin_to_mired(app.determine_color_temperature()))
                last_refresh = now

            if room_state_changed == True:
                simple_log("\033[1;36mRoom State:\033[0m \033[32m%s\033[0m\t\033[31m%s\033[0m" % (
                    [room_names[a] for a in enabled_rooms],
                    [room_names[b] for b in disabled_rooms]
                    ))

            sleep(2)
        except Exception, e:
            simple_log("Exception: %s" % e)
            traceback.print_exc()
        except KeyboardInterrupt, ki:
            sys.exit(1)
