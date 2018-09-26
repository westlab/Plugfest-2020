# -*- cording:utf-8 -*-

import time
import bluetooth
import select

def main():
    PORT =1
    server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    readfds = set([server_socket])

    print("connect...")

    try:
        server_socket.bind( ("",PORT ))
        server_socket.listen(1)

        while 1:
            rready, wready, xready = select.select(readfds, [], [])        
            for sock in rready:
                if sock is server_socket:
                    client_socket,address = server_socket.accept()
                    readfds.add(client_socket)
                    print("conecction secuccesful!!")
                else:
                    try:
                        msg = sock.recv(1024)
                    except KeyboardInterrupt:
                        for sock in readfds:
                            sock.close()
                    except:
                        sock.close()
                        readfds.remove(sock)
                        pass
                    finally:
                        if len(msg) == 0:
                            slck.close()
                            readfds.remove(sock)
                        else:
                            print(msg)
    finally:
        for sock in readfds:
            sock.close()
    return

if __name__ == '__main__':
    main()
