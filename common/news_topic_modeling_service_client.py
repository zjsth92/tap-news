import os
import sys
import yaml
import pyjsonrpc

with open(os.path.join(os.path.dirname(__file__), '..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)

RECOMMENDATION_SERVER_HOST = config["news_topic_modeling_service"]["host"]
RECOMMENDATION_SERVER_PORT = config["news_topic_modeling_service"]["port"]

URL = 'http://%s:%d' % (RECOMMENDATION_SERVER_HOST,RECOMMENDATION_SERVER_PORT)

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    print "Topic: %s" % str(topic)
    return topic
