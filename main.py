import os
import sys
from pigpio_dht import DHT11
import time
import ambient
import requests

DHT11_PIN = 14

CHANNEL = os.getenv("CHANNEL", default="")
WRITEKEY = os.getenv("WRITEKEY", default="")

Debugging = False
def DBG(*args):
    if Debugging:
        msg = " ".join([str(a) for a in args])
        print(msg)
        sys.stdout.flush()

Verbose = True
def MSG(*args):
    if Verbose:
        msg = " ".join([str(a) for a in args])
        print(msg)
        sys.stdout.flush()

def sendWithRetry(am, data):
    for retry in range(6):
        try:
            ret = am.send(data)
            MSG('sent to Ambient (ret = %d)' % ret.status_code)
            break
        except requests.exceptions.RequestException as e:
            MSG('request failed.')
            time.sleep(10)

am = ambient.Ambient(int(CHANNEL), WRITEKEY)
sensor = DHT11(DHT11_PIN)

while True:
    try:
        data = sensor.read(retries=5)
    except TimeoutError:
        data = {"valid": False}

    if data["valid"]:
        MSG("temperature: {} / humidity: {}".format(data["temp_c"], data["humidity"]))
        sendWithRetry(am, {'d1': data["temp_c"], 'd2': data["humidity"]})
    time.sleep(180)

