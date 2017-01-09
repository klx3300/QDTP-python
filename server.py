#!/usr/bin/env python3.5

import socket
import threading


def cli_conn_thread(sock, addr):
    print("New Connection Accepted from client addr:" , addr)
    # auth
    cli_psk = sock.recv(1024)
    with open("server_psk.psk", "rb") as pskf:
        srv_psk = pskf.read()
    if cli_psk != srv_psk:
        print(srv_psk,cli_psk)
        sock.send(b"044 Auth fail.")
        sock.close()
        return
    else:
        sock.send(b"080 Auth succ.")
    # receive operation value
    operation = sock.recv(1);
    if not (operation):
        print(b"Fatal Exception on sock.recv() . Stop.")
        return
    if operation == b'G':
        # receive filename
        filename = sock.recv(1024)
        # open file descor
        filedesc = open(filename, "rb")
        if not filedesc:
            sock.send(b"127 File not found.")
            sock.close()
            return
        sock.send(b"080 OK")
        rbuffer = filedesc.read(256)
        while rbuffer:
            sock.send(rbuffer)
            rbuffer = filedesc.read(256)
        # all data sent.
        # close connection
        filedesc.close()
        sock.close()
    elif operation == b"S":
        # receive file name
        filename = sock.recv(1024)
        # server ACK.
        # client won't send further data until the OK reached.

        filedesc = open(filename, "wb")
        if not filedesc:
            sock.send(b"290 Filesystem corruption or system resource fail.")
            sock.close()
            return
        sock.send(b"080 OK")
        wbuffer = sock.recv(256)
        while wbuffer:
            filedesc.write(wbuffer)
            try:
                wbuffer = sock.recv(256)
            except BaseException as e:
                wbuffer = None
        filedesc.close()
        sock.close()
    else:
        sock.send(b"71 ERROR. Unresolvable cli request")
        sock.close()


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('0.0.0.0', 4582))
listener.listen(5)
while True:
    sock, addr = listener.accept()
    threading.Thread(target=cli_conn_thread, args=(sock, addr)).start()
