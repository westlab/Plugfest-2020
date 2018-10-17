# -*- coding: utf-8 -*- 
from btle import Peripheral

from RN42 import RN42
from time import sleep

import struct 
import btle
import binascii
 
import RPi.GPIO as GPIO
import sys
import time
import re
import argparse
import requests
import random
import glob
from datetime import datetime

parser = argparse.ArgumentParser(
    prog = 'alps.py',
    usage = 'Receive BLE sensor data and send to NCAP with TEDS and TEXTTEDS (xml-based TEDS)',
    description= 'TIM for ALPS Smart IoT BLE Sensor module\nYou have to put TEDS files of required filenames to ../TEDS/ directory',
    epilog = 'Programmer Hiroaki Nishi west@west.yokohama',
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
parser.add_argument('-P', '--pseudo_sensor',
    action = 'store_true',
    help = 'generate random sensor values without ALPS module',
    default = False)
parser.add_argument('-m', '--alpsmodule',
    action = 'store',
    help = 'specify ALPS Smart IoT Module Bluetooth address',
    nargs = '?',
    default = '48:F0:7B:78:47:33',
    type = str)
parser.add_argument('-d', '--destination_address',
    action = 'store',
    help = 'specify destination Bluetooth address',
    nargs = '?',
    default = 'B8:27:EB:DB:D2:8E',
    type = str)
parser.add_argument('-E', '--elasticsearch',
    action = 'store_true',
    help = 'prepare elasticsearch/kibana data and push',
    default = False)
parser.add_argument('-e', '--elasticsearch_address',
    action = 'store',
    help = 'specify destination Bluetooth address',
    nargs = '?',
    default = 'http://localhost:9200/plugfest',
    type = str)

args = parser.parse_args()
vflag = False
if args.verbose:
    vflag = True
qflag = False
if args.quiet:
    qflag = True
eflag = False
if args.elasticsearch:
    eflag = True
pflag = False
if args.pseudo_sensor:
    pflag = True

def s16(value):
    return -(value & 0b1000000000000000) | (value & 0b0111111111111111)


class NtfyDelegate(btle.DefaultDelegate):
    GeoMagnetic_X = 0;
    GeoMagnetic_Y = 0;
    GeoMagnetic_Z = 0;
    Acceleration_X = 0;
    Acceleration_Y = 0;
    Acceleration_Z = 0;
    Pressure = 0;
    Humidity = 0;
    Temperature = 0;
    UV = 0;
    AmbientLight = 0;
    def __init__(self, params):
        btle.DefaultDelegate.__init__(self)
        # ... initialise here
 
    def handleNotification(self, cHandle, data): 
        # ... perhaps check cHandle
        # ... process 'data'
        cal = binascii.b2a_hex(data)
        #print u'handleNotification : {0}-{1}:'.format(cHandle, cal)
     
        if int((cal[0:2]), 16) == 0xf2:
            NtfyDelegate.GeoMagnetic_X = s16(int((cal[6:8] + cal[4:6]), 16)) * 0.15
            NtfyDelegate.GeoMagnetic_Y = s16(int((cal[10:12] + cal[8:10]), 16)) * 0.15
            NtfyDelegate.GeoMagnetic_Z = s16(int((cal[14:16] + cal[12:14]), 16)) * 0.15
            if vflag == True:
                print('Geo-Magnetic X:{0:.3f} Y:{1:.3f} Z:{2:.3f}'.format(NtfyDelegate.GeoMagnetic_X, NtfyDelegate.GeoMagnetic_Y, NtfyDelegate.GeoMagnetic_Z))
            NtfyDelegate.Acceleration_X = 1.0 * s16(int((cal[18:20] + cal[16:18]), 16)) / 1024
            NtfyDelegate.Acceleration_Y = 1.0 * s16(int((cal[22:24] + cal[20:22]), 16)) / 1024
            NtfyDelegate.Acceleration_Z = 1.0 * s16(int((cal[26:28] + cal[24:26]), 16)) / 1024
            if vflag == True:
                print('Acceleration X:{0:.3f} Y:{1:.3f} Z:{2:.3f}'.format(NtfyDelegate.Acceleration_X, NtfyDelegate.Acceleration_Y, NtfyDelegate.Acceleration_Z))

        if int((cal[0:2]), 16) == 0xf3:
            NtfyDelegate.Pressure = int((cal[6:8] + cal[4:6]), 16) * 860.0/65535 + 250
            NtfyDelegate.Humidity = 1.0 * (int((cal[10:12] + cal[8:10]), 16) - 896 )/64
            NtfyDelegate.Temperature = 1.0*((int((cal[14:16] + cal[12:14]), 16) -2096)/50)
            UV = int((cal[18:20] + cal[16:18]), 16) / (100*0.388)
            NtfyDelegate.AmbientLight = int((cal[22:24] + cal[20:22]), 16) / (0.05*0.928)
            if vflag == True:
                print('Pressure:{0:.3f} Humidity:{1:.3f} Temperature:{2:.3f} UV:{3:.3f} AmbientLight:{4:.3f} '.format(NtfyDelegate.Pressure, NtfyDelegate.Humidity, NtfyDelegate.Temperature, NtfyDelegate.UV, NtfyDelegate.AmbientLight))

class AlpsSensor(Peripheral):
    def __init__(self,addr):
        Peripheral.__init__(self,addr)
        self.result = 1
 
def main():
    if pflag == False:
        print("Turn On Sensor Node")
#       alps = AlpsSensor("48:F0:7B:78:47:33")
        alps = AlpsSensor(args.alpsmodule)
        alps.setDelegate( NtfyDelegate(btle.DefaultDelegate) )
    
    if eflag == True:
        response = requests.put(args.elasticsearch_address)
        if vflag == True:
            print(response.json())
 
    if pflag == False:
        #Hybrid MAG ACC8G 100ms / Other 1s
        alps.writeCharacteristic(0x0013, struct.pack('<bb', 0x01, 0x00), True)# Custom1 Notify Enable 
        alps.writeCharacteristic(0x0016, struct.pack('<bb', 0x01, 0x00), True)# Custom2 Notify Enable
        alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x2F, 0x03, 0x03), True)# (Non-volatile) Initialize stored data
        alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x01, 0x03, 0x7F), True)# Enalbe Geomagnetism, Acceleration, Puressure, Temparature, Humidity, UV, Illuminance
    #    alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x04, 0x03, 0x04), True)# Hybrid Mode
        alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x04, 0x03, 0x00), True)# Hybrid Mode
    #    alps.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x06, 0x04, 0x64, 0x00), True) # Fast 100msec (Geomagnetism,Acceleration)
    #    alps.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x06, 0x04, 0x7A, 0x01), True) # Fast 250msec (Geomagnetism,Acceleration) only Hybrid mode (deleted)
        alps.writeCharacteristic(0x0018, struct.pack('<bbbb', 0x05, 0x04, 0x01, 0x00), True) # Slow 1sec (Pressure, Temparature, Humidity, UV, Illuminance)
        alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x02, 0x03, 0x02), True) # Acceleration +-8G
        alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x2F, 0x03, 0x01), True)# Store configuration
        alps.writeCharacteristic(0x0018, struct.pack('<bbb', 0x20, 0x03, 0x01), True)# Sart measuremnt
        ## Setting & Connect
    ras = RN42("ras", args.destination_address, 1)
    ras.connectBluetooth(ras.bdAddr,ras.port)
     
# Main loop --------
    fileset = glob.glob("../TEDS/DATA-*.txt") 
    for fname in fileset:
        ftype = re.split('-', fname)
        with open(fname) as f:
            if qflag == False:
                print(fname+"=="+"#"+ftype[1]+":"+ftype[2])
            ras.sock.send("#"+ftype[1]+":"+ftype[2])
            msg = f.read()
            ras.sock.send(msg)
            if qflag == False:
                print("TEDS:"+msg)
    while True:
        (dt, micro) = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f').split('.')
        dt = "%s.%03d" % (dt, int(micro)/1000)
        if pflag == True:
            Pressure = 980.0+random.randint(2000,4000)/100.0
            Humidity = 20.0+random.randint(0,6000)/100.0
            Temperature = 18.0+random.randint(0,80000)/100.0
            AmbientLight = 0.0+random.randint(0,100000)/100.0
            UV = 0.0+random.randint(0,100000)/100.0
            GeoMagnetic_X = 0.0+random.randint(0,1000000)/100.0
            Acceleration_Y  = 0.0+random.randint(0,1000000)/100.0
            msg = '{{DATETIME:{0},PRESSURE:{1:.3f},HUMID:{2:.3f},TEMP:{3:.3f},ILLUMI:{4:.3f},UV:{5:.3f},GEOMAG:{6:.3f},ACCEL:{7:.3f}}}'.format(dt, Pressure, Humidity, Temperature, AmbientLight, UV, GeoMagnetic_X, Acceleration_Y)
            ras.sock.send(msg)
            sleep(1)
        else:
            try:
                n = alps.waitForNotifications(1.0)
            except KeyboardInterrupt:
                print("key pressed")
                sys.exit()
            except:
                pass
            if n:
                # handleNotification() was called
                msg = '{{DATETIME:{0},PRESSURE:{1:.3f},HUMID:{2:.3f},TEMP:{3:.3f},ILLUMI:{4:.3f},UV:{5:.3f},GEOMAG:{5:.3f},ACCEL:{6:.3f}}}'.format(dt, NtfyDelegate.Pressure, NtfyDelegate.Humidity, NtfyDelegate.Temperature, NtfyDelegate.AmbientLight, NtfyDelegate.UV, NtfyDelegate.GeoMagnetic_X, NtfyDelegate.Acceleration_Y)
                ras.sock.send(msg)
        if qflag == False:
            print("DATA:"+msg)
        if eflag == True:
            eheaders = {'Content-Type': 'application/json'}
            response = requests.post(args.elasticsearch_address, headers=eheaders, data=msg)
            if vflag == True:
                print(response.json())
            continue
    if vflag == True:
        print("Waiting...")
        # Perhaps do something else here
if __name__ == "__main__":
    main()
