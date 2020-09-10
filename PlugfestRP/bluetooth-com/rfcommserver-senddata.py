# -*- cording:utf-8 -*-

import time
import random
import time
import bluetooth

PORT =1
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

print("connect...")

server_socket.bind( ("",PORT ))
server_socket.listen(1)

client_socket,address = server_socket.accept()

print("conecction secuccesful!!")

while True:
  random_val = random.random()
  try:
    time.sleep(0.5)
    client_socket.send("data : " + str(random_val))
  except KeyboardInterrupt:
    client_socket.close()
    server_socket.close()
    break
  except Exception as ex:
    print("Unexpected error:", ex)
    client_socket.close()
    server_socket.close()
    break