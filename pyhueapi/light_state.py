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