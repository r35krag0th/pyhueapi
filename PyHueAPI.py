#!/usr/bin/python

import requests, json, sys
from time import sleep

class HueAPIBase(object):
    targetBridge = '10.0.42.18'
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
    def api_get(self, tokens=[], data={}):
        response = requests.get(self.getUrl(tokens), data=json.dumps(data))
        return response.json
    
    def api_put(self, tokens=[], data={}):
        #print "Tokens: %s" % tokens
        response = requests.put(self.getUrl(tokens), data=json.dumps(data))
        return response.json
        
    def api_post(self, tokens=[], data={}):
        response = requests.post(self.getUrl(tokens), data=json.dumps(data))
        return response.json
        
    def api_delete(self, tokens=[], data={}):
        response = requests.delete(self.getUrl(tokens), data=json.dumps(data))
        return response.json

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
        #| 1  | **Yes** | 79   | 33863 | 236 | 0.6271, 0.3297 | 154 |

        print "|%2s|%7s|%3s|%5s|%3s|%15s|%3s|" % (self.id, '**Yes**' if self.state.on else 'No', self.state.brightness, self.state.hue, self.state.saturation, self.state.xy, self.state.ct)
        
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
    
    def setColor(self, newX, newY):
        assert(newX > 0 and newX < 1)
        assert(newY > 0 and newY < 1)

        newValue = [newX, newY]
        if (newValue == self.state.xy): return
        
        self.api_put(tokens=[self.id, 'state'], data={'xy': newValue})
        
        self.state.xy = newValue
        
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
        
        self.on = data['on']
        self.brightness = int(data['bri'])
        self.hue = int(data['hue'])
        self.saturation = int(data['sat'])
        self.xy = data['xy']
        self.ct = int(data['ct'])
        self.alert = data['alert']
        self.effect = data['effect']
        self.colormode = data['colormode']
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
    for tmp in allLights:
        light = a.get(tmp)
        light._print_md()
        #light.setColor(0.4500, 0.2000)
        #sleep(1)
        
    sys.exit(1)
    
    print "*" * 80
    print ""
    print ""
    
    b = a.get(1)
    c = a.get(2)
    d = a.get(3)
    
    b._print()
    b.setBrightness(255)
    
    c._print()
    c.setBrightness(255)
    
    d._print()
    d.setBrightness(255)
    
    sleep(2)
    
    # TEST
    #for i in range(0,255):
    #    print i
    #    b.setBrightness(i)
    #    c.setBrightness(i)
    #    d.setBrightness(i)
    #    sleep(0.05)
    
    cycleColors = [
        [0.4500, 0.5000],
        [0.4500, 0.4500],
        [0.4500, 0.4000],
        [0.4500, 0.3500],
        [0.4500, 0.3200],
        [0.4500, 0.3000],
        [0.4500, 0.2500],
        [0.4500, 0.2000],
        [0.4500, 0.1500],
        [0.4500, 0.1000],
        [0.4500, 0.0800],
        [0.4500, 0.0600],
        [0.4500, 0.0400],
        [0.4500, 0.0200],
    ]
    for i in cycleColors:
        print i
        b.setColor(i[0], i[1])
        c.setColor(i[0], i[1])
        d.setColor(i[0], i[1])
        sleep(1)
        
    for i in cycleColors:
        print i
        b.setColor(i[1], i[0])
        c.setColor(i[1], i[0])
        d.setColor(i[1], i[0])
        sleep(1)