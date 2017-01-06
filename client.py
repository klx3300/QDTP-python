#!/usr/bin/env python3.5

import socket


# these functions will not close file descriptor for you!

def communicate_get(psk, filedesc, serveraddr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((serveraddr, 4582))
    # authentication
    sock.send(psk)
    repstr = sock.recv(1024)
    if repstr[:3]!="080":
        #cond not succ
        print(repstr)
        sock.close()
        return
    sock.send('G')
    repstr = sock.recv(3)
    if repstr != "080":
        #cond not succ
        extra = sock.recv(1024)
        print(repstr, extra)
        sock.close()
        return
    #cond succ
    repstr=sock.recv(3)
    wbuffer=sock.recv(256)
    while wbuffer:
        filedesc.write(wbuffer)
        sock.recv(256)
    sock.close()

def communicate_set(psk, filedesc, serveraddr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((severaddr,4582))
    # auth
    sock.send(psk)
    repstr = sock.recv(1024)
    if repstr[:3]!="808":
        #cond not succ
        print(repstr)
        sock.close()
        return
    sock.send('S')
    repstr = sock.recv(3)
    if repstr != '080':
        #cond not succ
        extra=sock.recv(1024)
        print(repstr, extra)
        sock.close()
        return
    #cond succ
    rbuffer = filedesc.read(256)
    while rbuffer:
        sock.send(rbuffer)
        rbuffer = filedesc.read(256)
    sock.close()
