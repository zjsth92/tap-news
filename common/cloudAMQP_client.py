import os
import json
import pika

with open(os.path.join(os.path.dirname(__file__), '..', 'config.json')) as config_file:    
    config = json.load(config_file)

class CloudAMQPClient:

    def __init__(self, cloud_amqp_url, queue_name):
        print "init cloud AMQP client name:%s" % queue_name
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        # set parameters
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = config["amqp"]["socket_timeout"]
        # create connection
        self.connection = pika.BlockingConnection(self.params)
        # create channel
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def sendMessage(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print "[X] Sent message to %s: %s" % (self.queue_name, message)
        return

    def getMessage(self):
        method, properties, body = self.channel.basic_get(self.queue_name)
        if method is not None:
            print "[O] Received message from %s: %s" % (self.queue_name, body)
            # ack message and delete
            self.channel.basic_ack(method.delivery_tag)
            return json.loads(body)
        else:
            print "No message returned"
            return None

    # sleep
    def sleep(self, seconds):
        self.connection.sleep(seconds)