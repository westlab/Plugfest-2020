# -*- cording:utf-8 -*-

import time
import bluetooth

PORT =1
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

print("connect...")

server_socket.bind( ("",PORT ))
server_socket.listen(1)

client_socket,address = server_socket.accept()

print("conecction secuccesful!!")

while 1:
  try:
    data = client_socket.recv(1024)
    print("receive [%s]" % data)
    print('\n')
  except KeyboardInterrupt:
    client_socket.close()
    server_socket.close()
    break
  except:
    print("error")
    print('\n')
    client_socket.close()
    server_socket.close()
    break
