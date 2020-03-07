#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from sys import stderr
from regserver_reg_db import access_reg_db
from regserver_regdetails_db import access_details_db
from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from pickle import load, dump

#--------------------------------------------------------------------------------

def handleClient(sock, clientAddr):
	inFlo = sock.makefile(mode='rb')
	specs = load(inFlo)
	print('Read from client ' + str(clientAddr))

	info_type = specs.pop("type", "list")
	if info_type == 'list': info = access_reg_db(specs)
	else: info = access_regdetails_db(specs)

	outFlo = sock.makefile(mode='wb')
	dump(info, outFlo)
	outFlo.flush()
	print('Wrote to client ' + str(clientAddr))

#--------------------------------------------------------------------------------

def execute_server(port):
	BACKLOG = 5

	try:
		serverSock = socket(AF_INET, SOCK_STREAM)
		print('Opened server socket')
		serverSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		serverSock.bind(('', port))
		print('Bound server socket to port')
		serverSock.listen(BACKLOG)
		print('Listening')

		while True:
			try:
				sock, clientAddr = serverSock.accept()
				print('Accepted connection for ' + str(clientAddr))
				print('Opened socket for ' + str(clientAddr))
				handleClient(sock, clientAddr)
				sock.close()
				print('Closed socket for ' + str(clientAddr))

			except Exception as e:
				print('regserver: ' + str(e), file=stderr)

	except Exception as e:
		print('regserver: ' + str(e), file=stderr)
