import requests, json

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
