# -*- coding: utf-8 -*-
# RN42.py
from time import sleep
import sys
import bluetooth

class RN42:
    def __init__(self, name, addr, num):
        """ Arduino with RN42"""
        self.__name = name     #Set Name
        self.__bdAddr = addr   #the address form the Arduino RN42
        self.__port = num      #Connect Port (RaspberryPi  to Arduino)
        self.__sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #config

    @property
    def name(self):
        pass
    @name.getter
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name

    @property
    def bdAddr(self):
        pass
    @bdAddr.getter
    def bdAddr(self):
        return self.__bdAddr
    @bdAddr.setter
    def bdAddr(self,value):
        self.__bdAddr = value
        return

    @property
    def port(self):
        pass
    @port.getter
    def port(self):
        return self.__port
    @port.setter
    def port(self,value):
        self.__port = value
        return

    @property
    def sock(self):
        pass
    @sock.getter
    def sock(self):
        return self.__sock
    @sock.setter
    def sock(self, value):
        self.__sock = value
    def reConnect(self, addr, num):
        self.__bdAddr = addr   #the address form the Arduino RN42
        self.__port = num      #Connect Port (RaspberryPi  to Arduino)
        self.__sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM) #config

    def connectBluetooth(self, bdAddr, port):
        while(1):
            try:
                print(self.__name + " : Connect......")
                self.__sock.connect((bdAddr,port))
                sleep(2)
                print(self.__name + " : Successful Connected!!!")
                break
            except bluetooth.BluetoothError :
                print(self.name + " : connecting failed")
                print("try connecting")
                self.reConnect(bdAddr, port)
                sleep(0.5)
            except KeyboardInterrupt:
                break

    def disConnect(self,sock):
        sock.close() 
