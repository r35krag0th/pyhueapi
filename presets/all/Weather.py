#!/usr/local/bin/python

import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.curdir, '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..', '..')))

import pyhueapi
from pyhueapi.preset import Preset
from time import sleep
import requests
from pyhueapi import irc_notification

def make_request(api_key=None, api_section=None):
    if None == api_key: api_key = '46806c0b6a4c2067'
    if None == api_section: api_section = 'conditions'

    target_url = 'http://api.wunderground.com/api/%s/%s/q/IL/Champaign.json' % (api_key, api_section)
    print target_url
    response = requests.get(target_url)

    if hasattr(response.json, '__call__'):
        return response.json()
    else:
        return response.json

def determine_color(temperature, shading_amount=0):
    # print "determine_color(temperature=%s, shading_amount=%s)" % (temperature, shading_amount)
    xy_blue = [0.1684, 0.0416]
    xy_yellow = [0.4083, 0.5162]
    xy_orange_light = [0.5093, 0.4428]
    xy_orange_deep = [0.6077, 0.3706]
    xy_red = [0.674, 0.322]

    target_color = None

    # blue   | temp <  65
    # yellow | temp >= 65 && temp < 75
    # or_lgh | temp >= 75 && temp < 80
    # or_dep | temp >= 80 && temp < 90
    # red    | temp >= 90
    temperature = int(temperature)
    # print "Temperature (int): %d" % temperature

    if temperature < 65:
        # print ">> blue"
        target_color = xy_blue
    elif temperature >= 65 and temperature < 75:
        # print ">> yellow"
        target_color = xy_yellow
    elif temperature >= 75 and temperature < 80:
        # print ">> orange (light)"
        target_color = xy_orange_light
    elif temperature >= 80 and temperature < 90:
        # print ">> orange (deep)"
        target_color = xy_orange_deep
    elif temperature >= 90:
        # print ">> red"
        target_color = xy_red

    ## Apply shading
    return [target_color[0] + shading_amount, target_color[1] + shading_amount]

if __name__ == '__main__':
    # Get some external data
    current_temperature = make_request(api_section='conditions')['current_observation']['temp_f']

    forecast_data = make_request(api_section='forecast')['forecast']['simpleforecast']['forecastday']
    today_forecast_high = forecast_data[0]['high']['fahrenheit']
    today_forecast_low  = forecast_data[0]['low']['fahrenheit']
    tomorrow_forecast_high = forecast_data[1]['high']['fahrenheit']
    tomorrow_forecast_low  = forecast_data[1]['low']['fahrenheit']

    print "Right now it is %s F" % current_temperature
    print "Today Forecast: %s to %s F" % (today_forecast_low, today_forecast_high)
    print "Tomorrow Forecast: %s to %s F" % (tomorrow_forecast_low, tomorrow_forecast_high)

    print '-' * 80
    print "Right Now  color: %s"    % determine_color(current_temperature)
    print "Today Low  color: %s"    % determine_color(today_forecast_low)
    print "Today High color: %s"    % determine_color(today_forecast_high)
    print "Tomorrow Low  color: %s" % determine_color(tomorrow_forecast_low)
    print "Tomorrow High color: %s" % determine_color(tomorrow_forecast_high)

    color_current_temperature = determine_color(current_temperature)
    color_today_low = determine_color(today_forecast_low)
    color_today_high = determine_color(today_forecast_high)
    color_tomorrow_low = determine_color(tomorrow_forecast_low)
    color_tomorrow_high = determine_color(tomorrow_forecast_high)

    target_preset = Preset()
    target_preset.parse_arguments()

    top_color = color_today_high
    mid_color = color_current_temperature
    bot_color = color_today_high

    target_preset.define_preset([
        {'id': 10, 'on': True, 'bri': 100, 'xy': top_color, 'transitiontime': 10000 },
        {'id': 2,  'on': True, 'bri': 100, 'xy': mid_color, 'transitiontime': 10000 },
        {'id': 12, 'on': True, 'bri': 100, 'xy': top_color, 'transitiontime': 10000 },
        ])
    target_preset.execute()
