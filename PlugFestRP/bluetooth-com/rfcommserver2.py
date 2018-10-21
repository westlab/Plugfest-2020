# -*- cording:utf-8 -*-

import time
import bluetooth
import select
import re
import argparse

import sys
from time import sleep
import paho.mqtt.client as mqtt
import random

parser = argparse.ArgumentParser(
    prog = 'alps.py',
    usage = 'Receive BLE sensor data and send to NCAP with TEDS and TXTTEDS (xml-based TEDS)',
    description= 'NCAP for TIM of ALPS Smart IoT BLE Sensor module\nYou have to install and communicate with supported TIM',
    epilog = 'Programmer: Hiroaki Nishi west@west.yokohama',
    add_help = True)
parser.add_argument('--version', version='%(prog)s 0.1',
    action = 'version',
    help = 'verbose operation (output sensor data)')
parser.add_argument('-v', '--verbose',
    action = 'store_true',
    help = 'verbose operation (output sensor data)',
    default = False)
parser.add_argument('-q', '--quiet',
    action = 'store_true',
    help = 'quiet (does not output data messages)',
    default = False)
parser.add_argument('-~', '--super_quiet',
    action = 'store_true',
    help = 'Perfectly quiet (does not output data messages)',
    default = False)
parser.add_argument('-c', '--connect',
    action = 'store',
    help = 'connect to MQTT server (mode ID can be specified [0:No TEDS 1:Dual topics 2:Single topic 3:Callback  Multiple designation is available)',
    choices = range(0,4),
    nargs = '*',
    default = [],
    type = int)
parser.add_argument('-P', '--pseudo_sensor',
    action = 'store_true',
    help = 'generate random sensor values without ALPS module',
    default = False)
parser.add_argument('-s', '--mqtt_server',
    action = 'store',
    help = 'specify MQTT server IP address',
    default = '131.113.98.77',
    type = str)
parser.add_argument('-p', '--mqtt_port',
    action = 'store',
    help = 'specify MQTT server port',
    default = 1883,
    type = int)
parser.add_argument('-k', '--mqtt_keepalive',
    action = 'store',
    help = 'specify MQTT keepalive timer (default is 15)',
    default = 15,
    type = int)
parser.add_argument('-t', '--topic',
    action = 'store',
    help = 'specify topic to publish (suffix is automatically added)',
    default = '/plugfest/westlab/',
    type = str)

args = parser.parse_args()
vflag = False
if args.verbose:
    vflag = True
qflag = False
if args.quiet:
    qflag = True
sqflag = False
if args.super_quiet:
    sqflag = True
pflag = False
if args.pseudo_sensor:
    pflag = True

global teds
def on_message(client, userdata, msg):
    data = msg.payload
    topic = msg.topic
    rdata = data.decode("utf-8")
    if sqflag == False:
        print("TEDSREQ:subscribed:TOPIC:"+topic)
        print("TEDSREQ:subscribed:MSG:"+data)
    if rdata.isalnum():
        stopic = re.sub('TEDSREQ$', 'TEDSRECV', topic)
        tedsname = re.sub('TEDSREQ$', '', topic)
        if teds[tedsname]:
            if sqflag == False:
                print("TEDSREQ:analyzed:TEDSNAME:"+tedsname)
            mqttc.publish(stopic, teds[tedsname], 0, retain=True)
            if sqflag == False:
                print("TEDSRECV:publish:TOPIC:"+stopic)
                print("TEDSRECV:publish:MSG:"+teds[tedsname])
        else:
            print("TEDSREQ: No registered TEDSNAME:"+tedsname)
            mqttc.publish(stopic, "ERR: No TEDS or SENSORS", 0, retain=True)
    else:
        print("TEDSREQ contains illegal character set")

def on_connect(client, userdata, msg):
    data = msg.payload
    topic = msg.topic
    rdata = data.decode("utf-8")
    if sqflag == False:
        print("Connect:TOPIC:"+topic)
        print("Connect:MSG:"+data)
    mqttc.subscribe(topic)

def on_publish(client, userdata, msg):
    if qflag == False:
        print("Published: "+str(msg))

def on_subscribe(client, userdata, msg, qos):
    # only when QoS is set
    if qflag == False:
        print("Subscribed: "+str(msg)+" "+str(qos))

def on_unsubscribe(client, userdata, msg):
    if qflag == False:
        print("UnSubscribed: "+str(msg))

def on_disconnect(client, userdata, msg):
    if msg != 0:
        print("Unexpected Disconnection")
    else:
        print("What's happen?")

def operation():
    try:
        server_socket.bind(("",server_port ))
        server_socket.listen(1)
        msg = ""
        teds = {}
        tedsreq = []
        peeraddr = "";

        while 1:
            rready, wready, xready = select.select(readfds, [], [])	
            for sock in rready:
                if sock is server_socket:
                    client_socket,address = server_socket.accept()
                    readfds.add(client_socket)
                    print("connected!:"+client_socket.getpeername()[0])
                else:
                    try:
                        msg = sock.recv(2048)
                    except KeyboardInterrupt:
                        for sock in readfds:
                            sock.close()
                    except:
                        sock.close()
                        readfds.remove(sock)
                        print("closed")
                        pass
                    finally:
                        try:
                            peer = sock.getpeername()
                        except:
                            peeraddr = "NA"
                        else:
                            peeraddr = peer[0]
                        if len(msg) == 0:
                            sock.close()
                            print("closed")
                            try:
                                readfds.remove(sock)
                            except:
                                pass
                        else:
                            if vflag == True:
                                print("RCV:"+str(len(msg)))
                if peeraddr == "NA2":
                    continue
                if qflag == False:
                    print(msg)
                if re.match("^#", msg): # for python 2.x
#                if re.match("^#", msg.decode(utf-8)): # for python 3.x
                    pmsg = msg[1:].split(':')
                    tname = pmsg[0]
                    name = pmsg[1]
                    if vflag == True:
                        print("TEDS="+msg)
                        print("TEDS TYPE="+tname)
                        print("TEDS NAME="+name)
                    msg = sock.recv(2048)
                    teds[name+tname] = msg
                    if vflag == True:
                        print("TEDS="+tname+"="+name+"="+msg)
                    tedsuri = args.topic+peeraddr+"/"+name+"/"+tname
                    tedsuris = args.topic+peeraddr+"/"+name
                    if 1 in args.connect:
                        # publish TEDS with retain bit
                        if qflag == False:
                            print("Publish[1]:"+tedsuri)
                        mqttc.publish(tedsuri, msg, 0, retain=True)
                    elif 2 in args.connect:
                        # publish TEDS with retain bit and data topic
                        if qflag == False:
                            print("Publish[2]:"+tedsuri)
                        mqttc.publish(tedsuris, msg, 0, retain=True)
                    elif 3 in args.connect:
                        # publish TEDS with handshake protocol
                        if qflag == False:
                            print("Publish[3]:"+tedsuri)
                        tedsreq.append((tedsuri+"/TEDSREQ", 0))
                        mqttc.subscribe(tedsreq)
                        if qflag == False:
                            print("Waiting TEDSREQ at ", tedsreq)
                    else:
                        print("Illegal MQTT mode.")

                else:
                    msg = msg[1:-1]
                    pmsg = msg.split(',')
                    for pmsgn in pmsg:
                        data = pmsgn.split(':')
                        if len(data) == 2:
                            if qflag == False:
                                print(data[0]+"="+data[1])
                            if args.connect:
                                #publish data[0] for data[1]
                                if qflag == False:
                                    print("Publish[data]:"+args.topic+peeraddr+"/"+data[0]+" as "+data[1])
                                mqttc.publish(args.topic+peeraddr+"/"+data[0], data[1])
    finally:
        for sock in readfds:
            sock.close()
    return

def pseudo_operation():
    # publish TEDS with retain bit
    address = "local"
    name = "pseudo_sensor"
    tname = "TEDS"
    msg = "6D40002004320000AA0107A1C0E00485953A3D0A660B928246586A56F3722DF93E124CCA0183933228A60000803F010040830100548500EA540773C1642FE654081C00"
    if vflag == True:
        print("TEDS TYPE="+tname)
        print("TEDS TYPE="+tname)
        print("TEDS NAME="+name)
    if args.connect:
        mqttc.publish(args.topic+address+"/"+name+"/"+tname, msg, 0, retain=True)
        print("Publish:"+args.topic+address+"/"+name+"/"+tname)
    else:
        print("Do nothing")
    #publish data
    while True:
        data = -10.0+random.randint(0,2000)/100.0
        if vflag == True:
            print("value="+str(data))
        if args.connect:
            if qflag == False:
                print("Publish:"+args.topic+address+"/"+name)
            mqttc.publish(args.topic+address+"/"+name, data)
        else:
            if qflag == False:
                print("Do nothing")
        sleep(1)

def main():
    global readfds, server_socket, server_port
    global mqttc
    server_port =1
    server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    readfds = set([server_socket])
    if qflag == False:
        print("System starts")

    if args.connect:
        mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
        mqttc.on_connect = on_connect
        mqttc.on_message = on_message
        mqttc.on_subscribe = on_subscribe
        mqttc.on_unsubscribe = on_unsubscribe
        mqttc.on_publish = on_subscribe
        mqttc.on_disconnect = on_disconnect
        mqttc.will_set('503 Service Unavailable')
        mqttc.connect(args.mqtt_server, port=args.mqtt_port, keepalive=args.mqtt_keepalive)
        if qflag == False:
            print("MQTT server ["+args.mqtt_server+"] connected")
    if qflag == False:
        print("waiting clients...")

    if pflag == False:
        operation()
    else:
        operation()

if __name__ == '__main__':
    main()
