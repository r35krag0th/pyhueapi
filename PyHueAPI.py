#!/usr/bin/python

import requests, json, sys, os
from time import sleep

class HueAPIBase(object):
    targetBridge = 'hue.r35.net'
    targetUser   = 'newdeveloper'

    #def __init__(self):
        #print "Initialized API Base"

    # Core
    def getUrl(self, tokens=[]):
        # Weed out lack of params vs params
        if not tokens == None and len(tokens) > 0 and not tokens[0] == None:
            tokens = [str(token) for token in tokens]
        else:
            tokens = []
        #print "GetUrl Tokens: %s" % tokens
        return 'http://%s/api/%s/%s/%s' % (self.targetBridge, self.targetUser, self.apiName, '/'.join(tokens) )

    ## Wrapped core methods
    def decide_output(self, someResponse):
        if hasattr(someResponse.json, '__call__'):
            return someResponse.json()
        else:
            return someResponse.json

    def api_get(self, tokens=[], data={}):
        response = requests.get(self.getUrl(tokens), data=json.dumps(data))
        return self.decide_output(response)

    def api_put(self, tokens=[], data={}):
        #print "Tokens: %s" % tokens
        response = requests.put(self.getUrl(tokens), data=json.dumps(data))
        return self.decide_output(response)

    def api_post(self, tokens=[], data={}):
        response = requests.post(self.getUrl(tokens), data=json.dumps(data))
        return self.decide_output(response)

    def api_delete(self, tokens=[], data={}):
        response = requests.delete(self.getUrl(tokens), data=json.dumps(data))
        return self.decide_output(response)

class Lights(HueAPIBase):
    apiName = 'lights'

    def __init__(self):
        super(Lights, self).__init__()
        #print "Initialized Lights"

    # Get all lights; or a specific light
    def getAll(self):
        response = self.api_get(tokens=[])
        return response

    def get(self, lightId=None):
        response = self.api_get(tokens=[lightId])
        #print response
        light = Light(lightId, response)
        return light

    # Get the result of the last search for new lights
    def new(self):
        response = self.api_get(tokens='new')
        print response

    # Start a search for new lights
    def search(self):
        response = self.api_post(tokens='new')

class Light(HueAPIBase):
    apiName = 'lights'
    id = 0

    ## Attributes / State
    state = None
    type = ''
    name = ''
    modelId = ''
    swVersion = ''
    pointSymbol = None

    def __init__(self, lightId, jsonData=None):
        super(Light, self).__init__()
        if jsonData == None: return
        self.id = int(lightId)
        self.state = LightState(jsonData['state'])
        self.type = jsonData['type']
        self.name = jsonData['name']
        self.modelId = jsonData['modelid']
        self.swVersion = jsonData['swversion']
        self.pointSymbol = jsonData['pointsymbol']

    def isOn(self):
        return self.state.on == True

    def _print(self):
        print "id=%d\tname=%20s\ton?=%s\t[ bri=%03d\thue=%05d\tsat=%03d ]\t[ xy=%s\tct=%s ]" % (self.id, self.name, self.state.on, self.state.brightness, self.state.hue, self.state.saturation, self.state.xy, self.state.ct)

    def _print_md(self):
        print "|%2s|%7s|%3s|%5s|%3s|%15s|%3s|" % (self.id, '**Yes**' if self.state.on else 'No', self.state.brightness, self.state.hue, self.state.saturation, self.state.xy, self.state.ct)

    def _print_preset(self):
        #print {'id': self.id, 'on': self.state.on, 'bri': self.state.brightness, 'sat': self.state.saturation, 'xy':self.state.xy, 'ct':self.state.ct, 'colormode':self.state.colormode}
        output =  {'on': self.state.on, 'bri': self.state.brightness}
        name_color = 32 if self.state.on else 37
        print "\033[37m%30s:\033[0m" % ('(#%d) \033[%sm%s' % (self.id, name_color, self.name)),
        value_color = 32 if self.state.on else 37

        if self.state.colormode == 'xy':
            output['xy'] = self.state.xy
            print '\033[36mxy=\033[%dm%s' % (value_color, self.state.xy),
        elif self.state.colormode == 'ct':
            # output['ct'] = self.state.ct
            print '\033[34mct=\033[%dm%d' % (value_color, self.state.ct),
        elif self.state.colormode == 'hs':
            try:
                print '\033[35mhue=\033[%dm%d \033[35msaturation=%s' % (value_color, self.state.hue, value_color, self.state.saturation),
            except Exception, e:
                pass
            output['hue'] = self.state.hue
            output['sat'] = self.state.saturation

        print '\033[33mbrightness=\033[%dm%d' % (value_color, self.state.brightness)


    def setHue(self, newHue):
        assert(newHue >= 0)
        assert(newHue <= 65535)

        if (newHue == self.state.hue): return

        self.api_put(tokens=[self.id, 'state'], data={'hue':newHue})

        self.state.hue = newHue

    def setBrightness(self, newBrightness):
        assert(newBrightness >= 0)
        assert(newBrightness <= 255)

        if (newBrightness == self.state.brightness): return

        self.api_put(tokens=[self.id, 'state'], data={'bri':newBrightness})

        self.state.brightness = newBrightness

    def setSaturation(self, newSaturation):
        assert(newSaturation > 0 and newSaturation <= 255)

        print ">>> Setting saturation to %d" % newSaturation

        self.api_put(tokens=[self.id, 'state'], data={'sat': newSaturation})
        self.state.saturation = newSaturation

    def setColor(self, newX, newY):
        assert(newX > 0 and newX < 1)
        assert(newY > 0 and newY < 1)

        newValue = [newX, newY]
        if (newValue == self.state.xy): return

        self.api_put(tokens=[self.id, 'state'], data={'xy': newValue})

        self.state.xy = newValue

    def setCt(self, newCt):
        self.api_put(tokens=[self.id, 'state'])

    def bulkSetState(self, rawData):
        if 'on' in rawData.keys() and not self.state.on == rawData['on']:
            self.api_put(tokens=[self.id, 'state'], data={'on':rawData['on']})

        # Make it look nicer
        if not 'transitiontime' in rawData.keys():
            # Default to 5 seconds
            rawData['transitiontime'] = 10 * 5

        self.api_put(tokens=[self.id, 'state'], data=rawData)
        self.state.bulkset(rawData)

        ## SYNC HERE
        sleep(0.05)

class LightState(object):
    on = False
    brightness = 0
    hue = 0
    saturation = 0
    xy = []
    ct = 0
    alert = 'none'
    effect = 'none'
    colormode = 'hs' # hs,xy,ct
    reachable = True # currently always true

    def __init__(self, data):
        if data == None: return
        self.bulkset(data)

    def set(self, stateKey, stateValue):
        if stateKey in ['bri', 'hue', 'sat', 'ct']:
            stateValue = int(stateValue)

        setattr(self, stateKey, stateValue)

    def bulkset(self, data):
        if 'on' in data:
            self.on = data['on']

        if 'bri' in data:
            self.brightness = int(data['bri'])

        if 'hue' in data:
            self.hue = int(data['hue'])

        if 'sat' in data:
            self.saturation = int(data['sat'])

        if 'xy' in data:
            self.xy = data['xy']

        if 'ct' in data:
            self.ct = int(data['ct'])

        if 'alert' in data:
            self.alert = data['alert']

        if 'effect' in data:
            self.effect = data['effect']

        if 'colormode' in data:
            self.colormode = data['colormode']

        if 'reachable' in data:
            self.reachable = data['reachable']

class Groups(HueAPIBase):
    apiName = 'groups'

    def __init__(self):
        super(Groups, self).__init__()
        print "Initialized Groups"

    def getAll(self):
        return self.api_get(tokens=[])

    def get(self, groupId):
        return Group(self.api_get(tokens=[groupId]))

class Group(HueAPIBase):
    apiName = 'groups'

    action = None
    lights = []
    name = ''

    def __init__(self, jsonData):
        super(Group, self).__init__()
        print "Initialized Group"

        if jsonData == None: return

        self.action = GroupAction(jsonData['action'])
        self.lights = jsonData['lights']
        self.name = jsonData['name']

class GroupAction(object):
    on = False
    brightness = 0
    hue = 0
    saturation = 0
    xy = []
    ct = 0
    effect = 'none'

    def __init__(self, data):
        if data == None: return

        self.on = data['on']
        self.brightness = int(data['bri'])
        self.hue = int(data['hue'])
        self.satuation = int(data['sat'])
        self.xy = data['xy']
        self.ct = int(data['ct'])
        self.effect = data['effect']

class Schedules(HueAPIBase):
    apiName = 'schedules'

    def __init__(self):
        super(Schedules, self).__init__()
        print "Initialized Schedules"

    def getAll(self):
        return self.api_get(tokens=[])

    def get(self, scheduleId):
        return Schedule(self.api_get(tokens=[scheduleId]))

    def create(self, scheduleObject):
        # type check this
        pass

    def delete(self, scheduleId):
        return self.api_delete(tokens=[scheduleId])

class Schedule(HueAPIBase):
    apiName = 'schedules'

    name = ""
    description = ""
    command = None
    time = None


    def __init__(self, jsonData):
        super(Schedule, self).__init__()
        print "Initialized Schedule"
        print jsonData
        self.name = jsonData['name']
        self.description = jsonData['description']
        self.command = ScheduleCommand(jsonData['command'])
        self.time = jsonData['time']

    def export(self):
        print "Stuff"

class ScheduleCommand(object):
    address = ""
    method = ""
    body = None

    def __init__(self, data):
        self.address = data['address']
        self.method = data['method']
        self.body = data['body']

class Configuration(HueAPIBase):
    def __init__(self):
        super(Configuration, self).__init__()
        print "Initialized Configuration"

class Portal(HueAPIBase):
    def __init__(self):
        super(Portal, self).__init__()
        print "Initialized Portal"

def make_changes(preset):
    if (os.path.exists('/tmp/pyhueapi.disable')): sys.exit(0)

    lights = Lights()
    for i in preset.keys():
        tmp = lights.get(i)
        data = preset[i]

        tmp.bulkSetState(data)

def compute_brightness_from_percentage(target_brightness_percent):
    if target_brightness_percent > 100 or target_brightness_percent < 0:
        print "You're bad at inputs.  0 < x < 100"
        sys.exit(1)

    return int(255 * (target_brightness_percent / 100.0))

if __name__ == '__main__':
    print "Main..."

    b = Groups()
    c = Schedules()
    d = Configuration()
    e = Portal()

    """
    print ""
    print "Lights"
    print "=" * 80
    a = Lights()
    a.getAll()
    returnedLight = a.get(1)
    print ""
    print returnedLight.id
    print returnedLight.state.on

    print ""
    print "Groups"
    print "=" * 80
    b = Groups()
    print b.getAll()
    """
    """
    print ""
    print "Schedules"
    print 80 * "="
    c = Schedules()
    print c.getAll()
    #for i in c.getAll():
    #    print i
    #    c.delete(i)

    #print c.get(24)
    """

    a = Lights()
    allLights = a.getAll()
    # for light in allLights.iteritems():
    #     print "%s is %s" % (light[0], light[1]['name'])

    collected_lights = {}

    for tmp in allLights:
        light = a.get(tmp)
        # light._print_preset()
        collected_lights['light_%02d' % light.id] = light

    collected_lights_keys = collected_lights.keys()
    collected_lights_keys.sort()
    for light_id in collected_lights_keys:
        # print light_id
        collected_lights[light_id]._print_preset()

    sys.exit(0)
