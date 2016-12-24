#!/usr/bin/env python3.5

import socket
import threading

def cli_conn_thread(sock,addr):
	print("New Connection Accepted from client addr:"+addr)
	# auth
	cli_psk=sock.recv(1024)
	with open("server_psk.psk","r") as pskf:
		srv_psk=pskf.read()
	if cli_psk!=srv_psk :
		sock.send("Auth fail.")
		sock.close()
		return
	else:
		sock.send("Auth succ.")
	# receive operation value
	operation=sock.recv(1);
	if !operation:
		print("Fatal Exception on sock.recv.Stop.")
		return
	if operation=='G':
		#receive filename len value
		filename=sock.recv(1024)
		#open file descor
		filedesc=open(filename,"rb")
		rbuffer=filedesc.read(256)
		while rbuffer:
			sock.send(rbuffer)
			rbuffer=filedesc.read(256)
		# all data sent.
		# close connection
		filedesc.close()
		sock.close()
	elif operation=="S":
		# receive file name
		filename=sock.recv(1024)
		#server ACK.
		#client won't send further data until the OK reached.
		sock.send("OK")
		filedesc=open(filename,"wb")
		wbuffer=sock.recv(256)
		while wbuffer:
			filedesc.write(wbuffer)
			wbuffer=sock.recv(256)
		filedesc.close()
		sock.close()
	else:
		sock.send("ERROR. Unresolvable cli request")
		sock.close()


listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
listener.bind(('0.0.0.0',4582))
listener.listen(5)
while True:
	sock,addr=listener.accept()
	threading.Thread(target=cli_conn_thread,args=(sock,addr)).start()

