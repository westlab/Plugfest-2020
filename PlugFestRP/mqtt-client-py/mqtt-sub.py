#! /usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
import  sys
from time import sleep
import paho.mqtt.client as mqtt

# ------------------------------------------------------------------
sys.stderr.write("*** START ***\n")
host = '192.168.8.101'
port = 1883
topic = 'topic_1'

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))

    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(msg.topic + ' ' + str(msg.payload,'utf-8'))

if __name__ == '__main__':

    client = mqtt.Client(protocol=mqtt.MQTTv311)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(host, port=port, keepalive=60)

    client.loop_forever()

sys.stderr.write("*** END ***\n")
# ------------------------------------------------------------------
