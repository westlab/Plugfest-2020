#!/usr/bin/python3
# -*- coding: utf-8 -*- 
from btle import Peripheral
import struct 
import btle
import binascii
import paho.mqtt.client as mqtt
import sys
import yaml
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
sqflag = False

f = open(args.config, "r+")
confdata = yaml.load(f)

host = confdata['mqtthost']
#'192.168.0.10'
port = confdata['mqttport']
#1883
topic = confdata['topic']+confdata['sensortopic']
#'/PRISM/SENSOR/'
 
def s16(value):
    return -(value & 0b1000000000000000) | (value & 0b0111111111111111)


class NtfyDelegate(btle.DefaultDelegate):
    def __init__(self, params, alpsid, cli):
        btle.DefaultDelegate.__init__(self)
        self.alpsid = alpsid
        self.cli = cli
        # ... initialise here
    def handleNotification(self, cHandle, data): 
        # ... perhaps check cHandle
        # ... process 'data'
        cal = binascii.b2a_hex(data)
        #print(u'handleNotification : {0}-{1}:'.format(cHandle, cal))
        if int((cal[0:2]), 16) == 0xf2:
            GeoMagnetic_X = s16(int((cal[6:8] + cal[4:6]), 16)) * 0.15
            GeoMagnetic_Y = s16(int((cal[10:12] + cal[8:10]), 16)) * 0.15
            GeoMagnetic_Z = s16(int((cal[14:16] + cal[12:14]), 16)) * 0.15
            print(self.alpsid, ':Geo-Magnetic X:{0:.3f} Y:{1:.3f} Z:{2:.3f}'.format(GeoMagnetic_X, GeoMagnetic_Y, GeoMagnetic_Z))
            self.cli.publish(topic+str(self.alpsid)+'/GEOMAGX', '{0:.3f}'.format(GeoMagnetic_X))
            self.cli.publish(topic+str(self.alpsid)+'/GEOMAGY', '{0:.3f}'.format(GeoMagnetic_Y))
            self.cli.publish(topic+str(self.alpsid)+'/GEOMAGZ', '{0:.3f}'.format(GeoMagnetic_Z))

            Acceleration_X = 1.0 * s16(int((cal[18:20] + cal[16:18]), 16)) / 1024
            Acceleration_Y = 1.0 * s16(int((cal[22:24] + cal[20:22]), 16)) / 1024
            Acceleration_Z = 1.0 * s16(int((cal[26:28] + cal[24:26]), 16)) / 1024
            print(self.alpsid, ':Acceleration X:{0:.3f} Y:{1:.3f} Z:{2:.3f}'.format(Acceleration_X, Acceleration_Y, Acceleration_Z))
            self.cli.publish(topic+str(self.alpsid)+'/ACCELX', '{0:.3f}'.format(Acceleration_X))
            self.cli.publish(topic+str(self.alpsid)+'/ACCELY', '{0:.3f}'.format(Acceleration_Y))
            self.cli.publish(topic+str(self.alpsid)+'/ACCELZ', '{0:.3f}'.format(Acceleration_Z))

        if int((cal[0:2]), 16) == 0xf3:
            Pressure = int((cal[6:8] + cal[4:6]), 16) * 860.0/65535 + 250	
            Humidity = 1.0 * (int((cal[10:12] + cal[8:10]), 16) - 896 )/64
            Temperature = 1.0*((int((cal[14:16] + cal[12:14]), 16) -2096)/50)
            UV = int((cal[18:20] + cal[16:18]), 16) / (100*0.388)
            AmbientLight = int((cal[22:24] + cal[20:22]), 16) / (0.05*0.928)
            print(self.alpsid, ':Pressure:{0:.3f} Humidity:{1:.3f} Temperature:{2:.3f} '.format(Pressure, Humidity , Temperature))
            self.cli.publish(topic+str(self.alpsid)+'/PRES', '{0:.3f}'.format(Pressure))
            self.cli.publish(topic+str(self.alpsid)+'/HUMID', '{0:.3f}'.format(Humidity))
            self.cli.publish(topic+str(self.alpsid)+'/TEMP', '{0:.3f}'.format(Temperature))
            print(self.alpsid, ':UV:{0:.3f} AmbientLight:{1:.3f} '.format(UV, AmbientLight))
            self.cli.publish(topic+str(self.alpsid)+'/UV', '{0:.3f}'.format(UV))
            self.cli.publish(topic+str(self.alpsid)+'/ILLUMI', '{0:.3f}'.format(AmbientLight))
 
class AlpsSensor(Peripheral):
    def __init__(self,addr):
        Peripheral.__init__(self,addr)
        self.result = 1

def main():
    print('start')
    if sys.version_info[0] != 3: 
        print("Version 3 is required") 
    print('MQTT setup')
    client = mqtt.Client(protocol=mqtt.MQTTv311)
    client.connect(host, port=port, keepalive=60)
    print('ALPS setup')
    alpsarray = []
    n = 1
    while True:
        keyname = 'alpsmodule'+str(n)
        if keyname in confdata:
            if confdata[keyname] is not None:
                print("No.%d : %s" % (n, confdata[keyname]))
                alpsarray.append(AlpsSensor(confdata[keyname]))
            n += 1
        else:
            break
#alpsmodule1: 48:F0:7B:78:47:25
#alpsmodule2: 48:F0:7B:78:47:33
#alpsmodule3: 48:F0:7B:78:47:35
#alpsmodule4: 48:F0:7B:78:47:36
#alpsmodule5: 48:F0:7B:78:47:4E
    for i,a in enumerate(alpsarray):
        a.setDelegate( NtfyDelegate(btle.DefaultDelegate, i+1, client) )
        print("node:",i+1)
 
        #Hybrid MAG ACC8G　100ms　/ Other 1s
        a.writeCharacteristic(0x0013, struct.pack('<bb', 0x01, 0x00), True)
        # Custom1 Notify Enable 
        a.writeCharacteristic(0x0016, struct.pack('<bb', 0x01, 0x00), True)
        # Custom2 Notify Enable
        a.writeCharacteristic(0x0018, struct.pack('<bbb', 0x2F, 0x03, 0x03), True)
        # (不揮発)保存内容の初期化
        a.writeCharacteristic(0x0018, struct.pack('<bbb', 0x01, 0x03, 0x7F), True)
        # 地磁気、加速度,気圧,温度,湿度,UV,照度を有効
        a.writeCharacteristic(0x0018, struct.pack('<bbb', 0x04, 0x03, 0x04), True)
        # Hybrid Mode
        # a.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x06, 0x04, 0x64, 0x00), True) # Fast 100msec (地磁気,加速度)
        a.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x06, 0x04, 0x7A, 0x01), True) 
        # Fast 250msec (地磁気,加速度)
        a.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x05, 0x04, 0x01, 0x00), True)
        # Slow 1sec (気圧,温度,湿度,UV,照度)     
        a.writeCharacteristic(0x0018, struct.pack('<bbb', 0x02, 0x03, 0x02), True)
        # 加速度±8G
        a.writeCharacteristic(0x0018, struct.pack('<bbb', 0x2F, 0x03, 0x01), True)
        # 設定内容保存
        a.writeCharacteristic(0x0018, struct.pack('<bbb', 0x20, 0x03, 0x01), True)
        # センサ計測開始
         
    # Main loop --------
    while True:
        for i,a in enumerate(alpsarray):
            if a.waitForNotifications(1.0):
                # handleNotification() was called
                continue

            print("Waiting...",i)
            # Perhaps do something else here
    client.disconnect()

if __name__ == '__main__':
    main()
