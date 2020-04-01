import http.client
import json
import random
import time

HOST = '0.0.0.0'
PORT = 3000
MESSAGE = 'test message {}'
PATH = 'log'

N_MESSAGES = 10

for _ in range(N_MESSAGES):
    client = http.client.HTTPConnection(HOST, PORT, timeout=0.01)
    message = MESSAGE.format(random.random())
    data = json.dumps({"message": message})
    client.request('POST', PATH, data, {"Content-Type": "application/json"})
    client.close()
    time.sleep(0.1)
