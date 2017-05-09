# -*- coding: utf-8 -*-
import os
import sys
import yaml
from newspaper import Article

import scraper

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

from cloudAMQP_client import CloudAMQPClient

with open(os.path.join(os.path.dirname(__file__), '..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)
    

# Use your own Cloud AMQP queue
DEDUPE_NEWS_TASK_QUEUE_URL = config["amqp"]["dedupe"]["url"]
DEDUPE_NEWS_TASK_QUEUE_NAME = config["amqp"]["dedupe"]["name"]
SCRAPE_NEWS_TASK_QUEUE_URL = config["amqp"]["scrape"]["url"]
SCRAPE_NEWS_TASK_QUEUE_NAME = config["amqp"]["scrape"]["name"]

SLEEP_TIME_IN_SECONDS = config["news_pipeline"]["fetcher"]["sleep_in_seconds"]
CUSTOM_SCRAPER_SOURCES = config["news_pipeline"]["fetcher"]["custom_scraper_sources"]

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

    if source in CUSTOM_SCRAPER_SOURCES:
        # if(source == "cnn" or source == "ew" or source == "espn"):
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
