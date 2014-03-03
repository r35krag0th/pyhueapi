import os, sys
from light import Light
from lights import Lights

def make_changes(preset, force=False):
    # Better handle this.
    if (os.path.exists('/tmp/pyhueapi.disable') and not force): sys.exit(0)

    lights = Lights()
    for i in preset:
        tmp = lights.get(i['id'])
        data = i
        data.pop('id')

        tmp.bulkSetState(data)

def compute_brightness_from_percentage(target_brightness_percent):
    if target_brightness_percent > 100 or target_brightness_percent < 0:
        print "You're bad at inputs.  0 < x < 100"
        sys.exit(1)

    return int(255 * (target_brightness_percent / 100.0))