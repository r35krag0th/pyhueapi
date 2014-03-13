from light import Light
from lights import Lights
import utils
from optparse import OptionParser

import os, sys

class Preset(object):
    lights = {}

    # "Lock file" for disabling
    disabled_lockfile = '/tmp/pyhueapi.disable'

    # on(True/False), hue/saturation(#/#) | xy([x,y]) | ct(#), bri(#)
    preset_details = []

    # Command-line flags
    options = None
    args = None

    parser = None
    forced_to_run = False
    is_disabled = False
    transition_time = 1
    brightness_override = 0

    def __init__(self):
        self.lights = Lights()

        # Global option parser for all the presets!
        self.parser = OptionParser()
        self.parser.add_option('-f', '--force', dest='forced_to_run', action='store_true', default=False, help='Force this preset to run, if we are disabled?')
        self.parser.add_option('-t', '--transition-time', dest='transition_time', action='store', metavar='seconds', default=5, type='int', help='How long should it take to transition to this preset (seconds)?')
        self.parser.add_option('-b', '--brightness', dest='brightness_override', action='store', metavar='percent', default=0, type='int', help='Override hard coded brightness with this value.')

    def _light_key(self, light_id):
        return 'hue_light#%d' % light_id

    def define_preset(self, presets):
        self.preset_details = []
        for preset in presets:
            preset_keys = preset.keys()

            #    | Making sure you gave a light_id to use
            if not 'id' in preset_keys:
                print "Missing 'id' in preset --> %s" % preset
                continue

            #    | Making sure you have at least one color mode used
            if (not 'xy' in preset_keys) and (not 'hue' in preset_keys and not 'sat' in preset_keys) and (not 'ct' in preset_keys):
                print "Invalid preset --> %s" % preset
                continue

            #    | Assuming you mean to turn the light on
            if not 'on' in preset_keys:
                preset['on'] = True

            #    | Default brightness if none given
            if not 'bri' in preset_keys:
                preset['bri'] = 100

            # -t | Transition Time override
            if not 'transitiontime' in preset_keys:
                preset['transitiontime'] = 10 * self.options.transition_time

            # -b | Brightness Override
            if self.options.brightness_override > 0:
                preset['bri'] = self.options.brightness_override

            ## Prepare to add this to the preset
            staged_preset = {
                'id': preset['id'],
                'on': preset['on'],
                'bri': utils.compute_brightness_from_percentage(preset['bri'])
            }

            # Mash together preset color modes
            for color_mode in ['xy', 'hue', 'sat', 'ct']:
                try:
                    staged_preset[color_mode] = preset[color_mode]
                except KeyError, ke:
                    pass

            self.preset_details.append(staged_preset)
        #print "Preset Added!"

    def parse_arguments(self):
        (self.options, self.args) = self.parser.parse_args()

    def execute(self):
        self.forced_to_run = self.options.forced_to_run
        self.transition_time = self.options.transition_time
        self.brightness_override = self.options.brightness_override

        if os.path.exists(self.disabled_lockfile):
            self.is_disabled = True

        if self.is_disabled and not self.forced_to_run:
            print "Presets are currently disabled.  Use -f to override."
            return

        utils.make_changes(self.preset_details, self.forced_to_run)

    def to_string(self):
        print 'HueControl Preset:'
        print '-' * 80

        sorted_keys = self.lights.keys()
        sorted_keys.sort()

        #for i in sorted_keys:
            #on_off_string = 'On' if data.
            #print "[ x ]"
