import os
import sys
import yaml
import pyjsonrpc

with open(os.path.join(os.path.dirname(__file__), '..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)

TOPIC_MODELING_SERVER_HOST = config["news_topic_modeling_service"]["server"]["host"]
TOPIC_MODELING_SERVER_PORT = config["news_topic_modeling_service"]["server"]["port"]

URL = 'http://%s:%d' % (TOPIC_MODELING_SERVER_HOST,TOPIC_MODELING_SERVER_PORT)

client = pyjsonrpc.HttpClient(url=URL)

def classify(text):
    topic = client.call('classify', text)
    print "Topic: %s" % str(topic)
    return topic
