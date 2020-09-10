#!/usr/bin/env python3

"""
This script creates an MQTT client that requests an NCAP to send TEDS.
"""

# Parameters
broker='127.0.0.1'
client_id='Application'
req_msg='Request TEDS'
res_topic='client/res'
teds_topic="NCAP/TEDS"
status_topic="NCAP/status"
msg_on='Online'
TIMEOUT=60.0

# Initialization
import asyncio
import datetime
from gmqtt import Client as MQTTClient
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
    msg=str(payload.decode("utf-8"))
    messages.append(msg)
    print('  Received message:', msg)
    print('  Properties in received message:', properties)

    # Proceed only if the NCAP alives
    if msg != msg_on:
        ask_exit()

def assign_callbacks_to_client(client):
  client.on_connect = on_connect
  client.on_message = on_message
  client.on_disconnect = on_disconnect

async def main(broker_host):
    client = MQTTClient(client_id)

    assign_callbacks_to_client(client)

    await client.connect(broker_host)

    print('Subscribe topic for the Last Will and Testament (LWT)...')
    client.subscribe(status_topic)

    print('Subscribe response topic...')
    client.subscribe(res_topic)

    print('Publish request message with response topic...')
    client.publish(teds_topic, req_msg, response_topic=res_topic)

    await STOP.wait()
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
      loop.run_until_complete(asyncio.wait_for(main(broker), TIMEOUT))
    except asyncio.TimeoutError:
      print('Timeout.')
