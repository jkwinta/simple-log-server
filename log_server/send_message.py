import http.client
import json
import random

HOST = '0.0.0.0'
PORT = 3000
MESSAGE = 'test message {}'.format(random.random())
PATH = 'log'

client = http.client.HTTPConnection(HOST, PORT, timeout=0.01)
data = json.dumps({"message": MESSAGE})
client.request('POST', PATH, data, {"Content-Type": "application/json"})
client.close()
