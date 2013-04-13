#!/usr/bin/python

import requests,json

class HueAPIBase(object):
    targetBridge = '10.0.42.18'
    targetUser   = 'newdeveloper'
    
    def __init__(self):
        print "Initialized API Base"
    
    # Core
    def getUrl(self, tokens=[]):
        # Weed out lack of params vs params
        if not tokens == None and len(tokens) > 0 and not tokens[0] == None:
            tokens = [str(token) for token in tokens]
        else:
            tokens = []
        print "GetUrl Tokens: %s" % tokens
        return 'http://%s/api/%s/%s/%s' % (self.targetBridge, self.targetUser, self.apiName, '/'.join(tokens) )
    
    ## Wrapped core methods
    def api_get(self, tokens=[], data={}):
        response = requests.get(self.getUrl(tokens), data=json.dumps(data))
        return response.json
    
    def api_put(self, tokens=[], data={}):
        print "Tokens: %s" % tokens
        requests.put(self.getUrl(tokens), data=json.dumps(data))
        return response.json
        
    def api_post(self, tokens=[], data={}):
        requests.post(self.getUrl(tokens), data=json.dumps(data))
        return response.json
        
    def api_delete(self, tokens=[], data={}):
        requests.delete(self.getUrl(tokens), data=json.dumps(data))
        return response.json

class Lights(HueAPIBase):
    apiName = 'lights'
    
    def __init__(self):
        super(Lights, self).__init__()
        print "Initialized Lights"
    
    # Get all lights; or a specific light
    def getAll(self):
        response = self.api_get(tokens=[])
        print response
        
    def get(self, lightId=None):
        response = self.api_get(tokens=[lightId])
        print response
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
        self.satuation = int(data['sat'])
        self.xy = data['xy']
        self.ct = int(data['ct'])
        self.alert = data['alert']
        self.effect = data['effect']
        self.colormode = data['colormode']
        self.reachable = if data['reachable']

class Groups(HueAPIBase):
    def __init__(self):
        super(Groups, self).__init__()
        print "Initialized Groups"
        
class Group(HueAPIBase):
    def __init__(self):
        super(Group, self).__init__()
        print "Initialized Group"
        
class Schedules(HueAPIBase):
    def __init__(self):
        super(Schedules, self).__init__()
        print "Initialized Schedules"

class Schedule(HueAPIBase):
    def __init__(self):
        super(Schedule, self).__init__()
        print "Initialized Schedule"

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
    
    a = Lights()
    b = Groups()
    c = Schedules()
    d = Configuration()
    e = Portal()
    
    a.getAll()
    returnedLight = a.get(1)
    print ""
    print returnedLight.id
    print returnedLight.state.on