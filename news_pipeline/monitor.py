# -*- coding: utf-8 -*-
import os
import sys
import yaml
import redis
import hashlib
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient

with open(os.path.join(os.path.dirname(__file__), '..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)

REDIS_HOST = config["redis"]["host"]
REDIS_PORT = config["redis"]["port"]

NEWS_TIME_OUT_IN_SECONDS = config["news_pipeline"]["monitor"]["news_timeout_in_seconds"]
SLEEP_TIME_IN_SECOUNDS = config["news_pipeline"]["monitor"]["sleep_in_seconds"]

# Use your own Cloud AMQP queue
SCRAPE_NEWS_TASK_QUEUE_URL = config["amqp"]["scrape"]["url"]
SCRAPE_NEWS_TASK_QUEUE_NAME = config["amqp"]["scrape"]["name"]

NEWS_SOURCES = [source.encode('ascii') for source in config["news_api"]["sources"]]

print 'monitor.py try to connect redis at %s:%d' % (REDIS_HOST, REDIS_PORT)
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
try:
    redis_client.get(None)  # getting None returns None or throws an exception
except (redis.exceptions.ConnectionError, 
        redis.exceptions.BusyLoadingError):
    print 'monitor.py redis connection Failed'
    exit(1)
print 'monitor.py redis connection success'


cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

while True:
    print "start monitor"
    print NEWS_SOURCES
    news_list = news_api_client.getNewsFromSource(NEWS_SOURCES)
    print "Get news %d" % len(news_list)
    num_of_new_news = 0

    for news in news_list:
        
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')

        if redis_client.get(news_digest) is None:
            num_of_new_news = num_of_new_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                # format: YYYY-MM-DDTHH:MM:SS in UTC
                news['publishedAt'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            redis_client.set(news_digest, news)
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d new news." % num_of_new_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECOUNDS)
