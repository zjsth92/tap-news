import os
import sys
import json
import pyjsonrpc
from pprint import pprint

with open(os.path.abspath('../config.json')) as config_file:    
    config = json.load(config_file)

SERVER_HOST = config["host"]
SERVER_PORT = config["port"]

class RequestHandler(pyjsonrpc.HttpRequestHandler):
    """ Test method """
    @pyjsonrpc.rpcmethod
    def add(self, a, b):
        print "add is called with %d and %d" % (a, b)
        return a + b

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (SERVER_HOST, SERVER_PORT),
    RequestHandlerClass = RequestHandler
)

print "Starting HTTP server on %s:%d" % (SERVER_HOST, SERVER_PORT)

http_server.serve_forever()