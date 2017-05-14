import os
import sys
import yaml

with open(os.path.join(os.path.dirname(__file__), '..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))

import mongodb_client
import news_topic_modeling_service_client

NEWS_TABLE_NAME = config["mongodb"]["news_table"]

if __name__ == '__main__':
    db = mongodb_client.get_db()
    cursor = db[NEWS_TABLE_NAME].find({})
    count = 0
    for news in cursor:
        count += 1
        print count
        print news
        if 'class' in news:
            print 'Populating classes...'
            text = news['title']
            topic = news_topic_modeling_service_client.classify(text)
            news['class'] = topic
            db[NEWS_TABLE_NAME].replace_one({'digest': news['digest']}, news, upsert=True)
