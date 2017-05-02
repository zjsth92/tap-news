# import common package in parent directory
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import news_topic_modeling_service_client as client

def test_basic():
    newsTitle = "Pentagon might propose ground troops for Syria"
    topic = client.classify(newsTitle)
    assert topic == "Politics & Government"
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
