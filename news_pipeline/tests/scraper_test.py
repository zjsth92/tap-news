import os
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import scraper

with open(os.path.join(os.path.dirname(__file__), "config.yaml"), 'r') as stream:
    config = yaml.load(stream)["test"]

def test_basic(source):
    print "test_basic for source:%s" % source
    url = config[source]["url"]
    espected_str = config[source]["expected_str"]
    news = scraper.extract_news(url, source)

    assert espected_str in news
    print news
    print 'test_basic for source:%s passed!' % source

def test_scraper(url, source):
    print "test_scraper for url:%s" % url
    news = scraper.extract_news(url, source)
    print news

if __name__ ==  "__main__":
    # for source in config["sources"]:
    #     test_basic(source)
    # url = "http://www.cnn.com/videos/politics/2017/05/02/gop-may-lose-health-care-vote-mattingly-tsr-dnt.cnn"
    url = "http://www.cnn.com/2017/05/02/politics/hillary-clinton-planned-parenthood/index.html"
    source = "cnn"
    test_scraper(url, source)