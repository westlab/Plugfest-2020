# -*- cording:utf-8 -*-

import time
import bluetooth
import select
import re
import argparse

import sys
from time import sleep
import paho.mqtt.client as mqtt

parser = argparse.ArgumentParser(
    prog = 'alps.py',
    usage = 'Receive BLE sensor data and send to NCAP with multipully formated TEDS',
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
parser.add_argument('-c', '--connect',
    action = 'store_true',
    help = 'connect to MQTT server',
    default = False)
parser.add_argument('-s', '--mqtt_server',
    action = 'store',
    help = 'specify MQTT server IP address',
    default = '131.113.98.77',
    type = str)
parser.add_argument('-p', '--mqtt_port',
    action = 'store',
    help = 'specify MQTT server port',
#    default = 1883,
    default = 57612,
    type = int)
parser.add_argument('-k', '--mqtt_keepalive',
    action = 'store',
    help = 'specify MQTT keepalive timer (default is 15)',
    default = 15,
    type = int)
parser.add_argument('-t', '--topic',
    action = 'store',
    help = 'specify topic to publish (suffix is automatically added)',
    default = '/plugfest/',
    type = str)

args = parser.parse_args()
vflag = False
if args.verbose:
    vflag = True
qflag = False
if args.quiet:
    qflag = True
cflag = False
if args.connect:
    cflag = True


def main():
    PORT =1
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    readfds = set([server_socket])

    if cflag == True:
        mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
        mqttc.connect(args.mqtt_server, port=args.mqtt_port, keepalive=args.mqtt_keepalive)
        if qflag == False:
            print("MQTT server connected")

    if qflag == False:
        print("waiting clients...")

    try:
	server_socket.bind( ("",PORT ))
	server_socket.listen(1)
	msg = ""
	teds = {}

	while 1:
	    rready, wready, xready = select.select(readfds, [], [])	
	    for sock in rready:
		if sock is server_socket:
		    client_socket,address = server_socket.accept()
		    readfds.add(client_socket)
		    print("connected! "+address[0])
		else:
		    try:
			msg = sock.recv(2048)
		    except KeyboardInterrupt:
			for sock in readfds:
			    sock.close()
		    except:
			sock.close()
			readfds.remove(sock)
			pass
		    finally:
			if len(msg) == 0:
			    sock.close()
			    readfds.remove(sock)
			else:
                            if vflag == True:
                                print("RCV:"+str(len(msg)))
		print(msg)
		if re.match("^#", msg):
                    pmsg = msg[1:].split(':')
		    tname = pmsg[0]
		    name = pmsg[1]
                    if vflag == True:
                        print("TEDS="+msg)
                        print("TEDS TYPE="+tname)
                        print("TEDS NAME="+name)
		    msg = sock.recv(2048)
		    teds[name] = msg
                    if vflag == True:
                        print("TEDS="+tname+"="+name+"="+msg)
                    if cflag == True:
                        # publish TEDS with retain bit
                        print(args.topic+address[0]+"/"+name+"/"+tname)
                        mqttc.publish(args.topic+address[0]+"/"+name+"/"+tname, msg, 0, retain=True)
		else:
                    msg = msg[1:-1]
		    pmsg = msg.split(',')
		    for pmsgn in pmsg:
			data = pmsgn.split(':')
			if (len(data) ==2) and (qflag == False):
                            print(data[0]+"="+data[1])
                            #publish data[0] for data[1]
                            if cflag == True:
                                mqttc.publish(args.topic+address[0]+"/"+data[0], data[1])
    finally:
	for sock in readfds:
	    sock.close()
    return

if __name__ == '__main__':
    main()
