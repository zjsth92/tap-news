import json
import os
import sys
import pyjsonrpc

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)

RECOMMENDATION_SERVER_HOST = config["recommendation_service"]["host"]
RECOMMENDATION_SERVER_PORT = config["recommendation_service"]["port"]

URL = 'http://%s:%d' % (RECOMMENDATION_SERVER_HOST,RECOMMENDATION_SERVER_PORT)

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    print "Preference list: %s" % str(preference)
    return preference
