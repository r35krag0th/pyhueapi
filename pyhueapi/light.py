from api_base import HueAPIBase
from light_state import LightState
from time import sleep

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
            print '\033[35mhue=\033[%dm%d \033[35msaturation=%s' % (value_color, self.state.hue, value_color, self.state.saturation),
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