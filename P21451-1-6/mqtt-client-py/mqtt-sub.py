#! /usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
import  sys
from time import sleep
import paho.mqtt.client as mqtt

# ------------------------------------------------------------------
sys.stderr.write("*** START ***\n")
#host = '192.168.8.101'
host = '131.113.98.77'
port = 1883
topic = '/TEST'

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload,'utf-8'))

if __name__ == '__main__':
    if sys.version_info[0] != 3:
        print("Version 3 is required")
        sys.exit()

#    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port, 60)

    client.loop_forever()

sys.stderr.write("*** END ***\n")
# ------------------------------------------------------------------
