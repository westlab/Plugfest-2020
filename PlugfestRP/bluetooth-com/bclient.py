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
    while 1:
	    ras.connectBluetooth(ras.bdAddr,ras.port)

	    print("Entering main loop now")

	    while 1:
		print("Loop")
		try:
		    print("Bef")
		    ras.sock.send("DATA to C7 from 50")
		    print("data send")
		    data = ras.sock.recv(1024)
		    print("receive [%s]" % data)
		    time.sleep(1)
		except KeyboardInterrupt:
		    print("Key")
		    ras.disconnect(ras.sock)
		except IOError:
		    print("Error")
		    break
		except:
		    print("error")
		    print("\n")
		    break

