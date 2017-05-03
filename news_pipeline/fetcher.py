# -*- coding: utf-8 -*-

import os
import sys
import json

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

# import scraper
import scraper

from cloudAMQP_client import CloudAMQPClient

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)
    

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = config["amqp"]["dedupe"]["url"]
DEDUPE_NEWS_TASK_QUEUE_NAME = config["amqp"]["dedupe"]["name"]
SCRAPE_NEWS_TASK_QUEUE_URL = config["amqp"]["scrape"]["url"]
SCRAPE_NEWS_TASK_QUEUE_NAME = config["amqp"]["scrape"]["name"]

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)

def handle_message(msg):
    if msg is None or not  isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg
    source = task['source']
    source_url = task['url']
    article_text = ""

    if(source == "cnn" or source == "ew" or source == "espn"):
        print "#### CUSTOM SCRAPER: URL:%s, SOURCE:%s ..." % (source_url, source)
        article_text = scraper.extract_news(source_url, source)
    else:
        article = Article(source_url)
        article.download()
        print "#### NEWSPAPER SCRAPER: URL:%s ..." % source_url
        article.parse()
        article_text = article.text
    
    if article_text:
        task['text'] = article_text
        dedupe_news_queue_client.sendMessage(task)
    else:
        print "#### SCRAPER cannot fetcher article at URL:%s" % source_url

while True:
    # fetch msg from queue
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            # Handle message
            try:
                handle_message(msg)
            except Exception as e:
                print e
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
