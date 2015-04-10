from api_base import HueAPIBase
from light import Light

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
        try:
            light = Light(lightId, response)
            return light
        except Exception, e:
            return None

    # Get the result of the last search for new lights
    def new(self):
        response = self.api_get(tokens='new')
        print response

    # Start a search for new lights
    def search(self):
        response = self.api_post(tokens='new')
