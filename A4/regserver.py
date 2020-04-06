#!/usr/bin/env python

#--------------------------------------------------------------------------------
# regserver.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from database import Database
from socket import socket
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from pickle import load, dump
from time import sleep
from sys import argv, stderr, exit

#--------------------------------------------------------------------------------

def report_err(msg):
	print('regserver: '+msg, file=sys.stderr)
	exit(1)

#--------------------------------------------------------------------------------

def check_input():
	if len(argv) != 3: report_err('Usage: python %s port delay' % argv[0])
	if not argv[1].isdigit(): report_err('port must be an integer')
	return int(argv[1]), int(argv[2])

#--------------------------------------------------------------------------------

def handleClient(sock, clientAddr, delay):
	inFlo = sock.makefile(mode='rb')
	specs = load(inFlo)
	print('Read from client ' + str(clientAddr))

	info_type = specs.pop("type", "list")
	database = Database()
	if info_type == 'list': info = database.search(specs)
	else: info = database.get_details(specs)

	sleep(delay)
	outFlo = sock.makefile(mode='wb')
	dump(info, outFlo)
	outFlo.flush()
	print('Wrote to client ' + str(clientAddr))

#--------------------------------------------------------------------------------

def execute_server(port, delay):
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
				handleClient(sock, clientAddr, delay)
				sock.close()
				print('Closed socket for ' + str(clientAddr))

			except Exception as e:
				print('regserver: ' + str(e), file=stderr)

	except Exception as e:
		print('regserver: ' + str(e), file=stderr)

#--------------------------------------------------------------------------------

def main():
	port, delay = check_input()
	execute_server(port, delay)

#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()