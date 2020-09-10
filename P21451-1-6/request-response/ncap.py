#!/usr/bin/env python3

"""
This script creates an MQTT client as an NCAP that provides TEDS at teds_topic.
"""

# Parameters
broker='127.0.0.1'
client_id='NCAP'
teds_topic="NCAP/TEDS"
teds_msg="TEDS information from NCAP"
status_topic="NCAP/status"
msg_on='Online'
msg_off='Offline'
msg_dead='Offline(dead)'
will_delay=2

# Mode
keep_connected=True

# Initialization
import asyncio
import gmqtt
messages=[]
STOP = asyncio.Event()

def ask_exit(*args):
    STOP.set()

def on_connect(client, flags, rc, properties):
    print('Connected with flags:',flags)

def on_disconnect(client, packet, exc=None):
    print('Disconnected.')

def on_message(client, topic, payload, qos, properties):
    print('Message received.')

    print('Properties in received message:', properties)
    response_topic = properties['response_topic'][0]
    print('Response topic in received message:', response_topic)

    print('Publish response message to response topic...')
    client.publish(response_topic, teds_msg)
    print('Published.')
    if not keep_connected:
      ask_exit()

def on_subscribe(client, mid, qos, properties):
    print('Subscribed.')

def assign_callbacks_to_client(client):
  client.on_connect = on_connect
  client.on_message = on_message
  client.on_disconnect = on_disconnect
  client.on_subscribe = on_subscribe

async def main(broker_host):
    will_message = gmqtt.Message(status_topic, msg_dead, retain=True, will_delay_interval=will_delay)
    client = gmqtt.Client(client_id, will_message=will_message)

    assign_callbacks_to_client(client)
    await client.connect(broker_host)

    print('Publish message indicating current status...')
    client.publish(status_topic, msg_on, retain=True)

    print('Subscribe topic to receive request messages...')
    client.subscribe(teds_topic, no_local=True)
    await STOP.wait()
    client.publish(status_topic, msg_off, retain=True)
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(broker))
