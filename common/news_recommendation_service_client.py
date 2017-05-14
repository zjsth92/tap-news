import yaml
import os
import sys
import pyjsonrpc

with open(os.path.join(os.path.dirname(__file__), '..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)

RECOMMENDATION_SERVER_HOST = config["news_recommendation_service"]["host"]
RECOMMENDATION_SERVER_PORT = config["news_recommendation_service"]["port"]

URL = 'http://%s:%d' % (RECOMMENDATION_SERVER_HOST,RECOMMENDATION_SERVER_PORT)

client = pyjsonrpc.HttpClient(url=URL)

def getPreferenceForUser(userId):
    preference = client.call('getPreferenceForUser', userId)
    print "Preference list: %s" % str(preference)
    return preference
