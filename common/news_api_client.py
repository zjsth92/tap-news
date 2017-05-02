import os
import json
import requests

from json import loads

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)
    config = config["newsApi"]

NEWS_API_ENDPOINT = config["endpoint"]
# Use your own API KEY
NEWS_API_KEY = config["key"]
DEFAULT_ARTICALS_TYPE = "articles"

DEFAULT_SOURCES = ['cnn']

SORT_BY_TOP = 'top'

def buildUrl(api_name=DEFAULT_ARTICALS_TYPE):
    return config["endpoint"] + api_name

def getNewsFromSource(sources=DEFAULT_SOURCES, sortBy=SORT_BY_TOP):
    articles = []
    for source in sources:
        payload = {'apiKey' : NEWS_API_KEY,
                   'source' : source,
                   'sortBy' : sortBy}
        response = requests.get(buildUrl(), params=payload)
        res_json = loads(response.content)

        # Extract info from response
        if (res_json is not None and
            res_json['status'] == 'ok' and
            res_json['source'] is not None):
            # populate news
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])
            
    return articles
