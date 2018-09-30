# -*- cording:utf-8 -*-

import time
import bluetooth
import select
import re

def main():
    PORT =1
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    readfds = set([server_socket])

    print("connect...")

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
                    print("connected!")
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
                            print("RCV:"+str(len(msg)))
                print(msg)
                if re.match("^#", msg):
                    name = msg[1:]
                    print("TEDS="+name)
                    msg = sock.recv(2048)
                    teds[name] = msg
                    print("TEDS="+name+"="+msg)
                    # publish TEDS with retain bit
                else:
                    pmsg = msg.split(',')
                    for pmsgn in pmsg:
                        data = pmsgn.split(':')
                        if(len(data) ==2):
                            print(data[0]+"="+data[1])
                            #publish data[0] for data[1]
    finally:
        for sock in readfds:
            sock.close()
    return

if __name__ == '__main__':
    main()
