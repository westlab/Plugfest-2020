# -*- coding: utf-8 -*-
# Main.py
from RN42 import RN42
from time import sleep
import RPi.GPIO as GPIO
import sys
import time

class Main:
    #"""" Main Class """

    ## Setting & Connect
    ras = RN42("ras", "B8:27:EB:9A:A4:C7", 1)
    ras.connectBluetooth(ras.bdAddr,ras.port)

    print("Entering main loop now")

    while 1:
        try:
            ras.sock.send("Hello World 50")
            print("data send")
            time.sleep(1)
        except KeyboardInterrupt:
            ras.disconnect(ras.sock)
