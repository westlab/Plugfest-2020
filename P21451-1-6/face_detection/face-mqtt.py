# -*- coding: utf-8 -*- 
import sys
import paho.mqtt.client as mqtt
import yaml
import re
import argparse

parser = argparse.ArgumentParser(
    prog = 'alpsmqtt.py',
    usage = 'Receive BLE sensor data and send to MQTT server',
    description= 'PRISM demo for ALPS Smart IoT BLE Sensor module\nYou have to install and Bluetooth modules',
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
parser.add_argument('-c', '--config',
    action = 'store',
    help = 'specify YAML config file',
    default = '../config.yml',
    type = str)

args = parser.parse_args()
vflag = False
if args.verbose:
    vflag = True
qflag = False
if args.quiet:
    qflag = True

f = open(args.config, "r+")
confdata = yaml.load(f)

host = confdata['mqtthost']
#'192.168.0.10'
port = confdata['mqttport']
#1883
topic = confdata['topic']+confdata['persontopic']
#'/PRISM/PERSON/'
rstrp = r'^\[(\d+),(\d+)\] .*, prob = ([\d\.]+)\s+(\(.*\)).*'
rstrpc = re.compile(rstrp)
rstrg = r'^Predicted g.* = ([MF]),(\d+).*'
rstrgc = re.compile(rstrg)
rstre = r'^Predicted e.* = (\w+).*'
rstrec = re.compile(rstre)
rstrh = r'^Head.* = ([\d\.\-\;]+).*'
rstrhc = re.compile(rstrh)

while True:
    di = input()
    if(di == "Press any key to stop"):
        break

def main():
    print('start')
    if sys.version_info[0] != 3: 
        print("Version 3 is required") 
    print('MQTT setup')
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(host, port=port, keepalive=60)
    di = input()
    while True:
        n = 0
        person = []
        if vflag:
            print('1:'+di)
        res = rstrpc.match(di)
        if res:
            while True:
                n += 1
                if vflag:
                    print(res.groups())
                person.append(res.groups())
                di = input()
                if vflag:
                    print('2:'+di)
                res = rstrpc.match(di)
                if res:
                    person.append(res.groups())
                else:
                    break
            for i in range(n):
                res = rstrgc.match(di)
                person[i] += res.groups()
                di = input()
                if vflag:
                    print('3:'+di)
                res = rstrec.match(di)
                person[i] += res.groups()
                di = input()
                if vflag:
                    print('4:'+di)
                res = rstrhc.match(di)
                person[i] += res.groups()
                if i < n:
                    di = input()
        for i in range(n, 5):
            if vflag:
                print(i)
            person.append((str(i), '0', '', '', '', '', '', ''))

        for i in range(len(person)):
#('0', '1', '1', '(436,204)-(730,730)', 'M', '34', 'surprise', '-8.31491;4.88977;-8.24657') 
            if len(person[i]) != 8:
                continue
            print('PUB:', end='')
            print(i,person[i])
            psersonid = str(int(person[i][0])+1)
            client.publish(topic+psersonid+'/PROB', person[i][2])
            client.publish(topic+psersonid+'/AREA', person[i][3])
            client.publish(topic+psersonid+'/GENDER', person[i][4])
            client.publish(topic+psersonid+'/AGE', person[i][5])
            client.publish(topic+psersonid+'/EMOTION', person[i][6])
            fx, fy, fz = person[0][7].split(';')
            client.publish(topic+psersonid+'/FACEX', fx)
            client.publish(topic+psersonid+'/FACEY', fy)
            client.publish(topic+psersonid+'/FACEZ', fz)
    client.disconnect()

if __name__ == '__main__':
    main()

