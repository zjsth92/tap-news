import yaml
import sys
import os
# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from cloudAMQP_client import CloudAMQPClient

with open(os.path.join(os.path.dirname(__file__), '../..', "config.yaml"), 'r') as config_file:
    config = yaml.load(config_file)

# Use your own URL
CLOUDAMQP_URL = config["amqp"]["url"]

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    # client.sleep(10)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed!'

if __name__ == "__main__":
    test_basic()
