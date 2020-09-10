#! /usr/bin/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
import  sys
from time import sleep
import paho.mqtt.client as mqtt

# ------------------------------------------------------------------

sys.stderr.write("*** START ***\n")

host = '10.1.1.24'
port = 1883
topic = '/plugfest/hoge'

if sys.version_info[0] != 3: 
    print("Version 3 is required") 

client = mqtt.Client(protocol=mqtt.MQTTv311)

client.connect(host, port=port, keepalive=60)

client.publish(topic, 'Good Afternoon')
sleep(0.5)
client.publish(topic, 'こんにちは')

client.disconnect()

sys.stderr.write("*** END ***\n")
# ------------------------------------------------------------------
