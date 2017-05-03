# -*- coding: utf-8 -*-

import os
import random
import requests
import yaml
from lxml import html

with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'r') as stream:
    config = yaml.load(stream)["scraper"]

# Load user agents
USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

def getHeaders():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection" : "close",
        "User-Agent" : ua
    }
    return headers

def extract_news(news_url, source):
    # Fetch html
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeaders())

    news = {}

    try:
        # Parse html
        tree = html.fromstring(response.content)

        # Extract information
        xpath = config[source]["xpath"]
        news = tree.xpath(xpath)
        news = ''.join(news)
    except Exception as e:
        print e
        return {}

    return news

