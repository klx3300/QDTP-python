#!/usr/bin/env python3.5

import socket


# these functions will not close file for you!

def communicate_get(psk, filename, filedesc, serveraddr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serveraddr, 4582))
    # authentication
    sock.send(psk)
    repstr = bytes.decode(sock.recv(1024))
    if repstr[:3]!="080":
        #cond not succ
        print(repstr)
        sock.close()
        return
    sock.send(b'G')
    sock.send(filename)
    repstr = bytes.decode(sock.recv(3))
    if repstr != "080":
        #cond not succ
        extra = bytes.decode(sock.recv(1024))
        print(repstr, extra)
        sock.close()
        return
    #cond succ
    repstr=bytes.decode(sock.recv(3))
    wbuffer=sock.recv(256)
    while wbuffer:
        filedesc.write(wbuffer)
        try:
            wbuffer = sock.recv(256)
        except BaseException as e:
            wbuffer = None
    sock.close()

def communicate_set(psk, filename, filedesc, serveraddr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serveraddr,4582))
    # auth
    sock.send(psk)
    repstr = bytes.decode(sock.recv(1024))
    if repstr[:3]!="080":
        #cond not succ
        print(repstr)
        sock.close()
        return
    sock.send(b'S')
    sock.send(filename)
    repstr = bytes.decode(sock.recv(3))
    if repstr != '080':
        #cond not succ
        extra=bytes.decode(sock.recv(1024))
        print(repstr, extra)
        sock.close()
        return
    #cond succ
    rbuffer = filedesc.read(256)
    while rbuffer:
        sock.send(rbuffer)
        rbuffer = filedesc.read(256)
    sock.close()
