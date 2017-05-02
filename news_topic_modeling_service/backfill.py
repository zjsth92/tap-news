import os
import sys
import json

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)

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
        if 'class' in news:
            print 'Populating classes...'
            title = news['title']
            topic = news_topic_modeling_service_client.classify(title)
            news['class'] = topic
            db['news'].replace_one({'digest': news['digest']}, news, upsert=True)
