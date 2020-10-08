import csv
import pprint
import asyncio
import os
import signal
import time
import uvloop
from gmqtt import Client as MQTTClient

TOPIC = 'Plugfest/keio/smartagri/'
TIMEOUT = 30
host = '192.168.0.10'

# gmqtt also compatibility with uvloop
#asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# STOP = asyncio.Event()

def on_connect(client, flags, rc, properties):
    print('Connected')
#    client.subscribe('TEST/#', qos=0)

#def on_message(client, topic, payload, qos, properties):
#    print('RECV MSG:', payload)


def on_disconnect(client, packet, exc=None):
    print('Disconnected')

#def on_subscribe(client, mid, qos, properties):
#    print('SUBSCRIBED')

#def ask_exit(*args):
#    STOP.set()

async def main(host):
    client = MQTTClient("smart-agri-data-publisher")
    #    client.on_connect = on_connect
    #    client.on_message = on_message
    client.on_disconnect = on_disconnect
    #    client.on_subscribe = on_subscribe

    #client.set_auth_credentials(token, None)
    #await client.connect(broker_host)
    await client.connect(host)
    with open('./20200701_0830_Outdoor-utf8.csv') as f:
        reader = csv.reader(f)
        readeri = iter(reader)
        next(readeri)
        header = next(readeri)
        print(header)
        next(readeri)
        while True:
            for row in reader:
                print(row)
                client.publish(TOPIC+header[0], str(row[0]), qos=1)
                time.sleep(5)

    await STOP.wait()
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
      loop.run_until_complete(asyncio.wait_for(main(host), TIMEOUT))
    except asyncio.TimeoutError:
      print('Timeout.')

