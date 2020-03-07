#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from reg_check import report_err
from socket import socket
from socket import AF_INET, SOCK_STREAM
from pickle import load, dump

#--------------------------------------------------------------------------------

def execute_client(host, port, specs):
	try:
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((host, port))
		outFlo = sock.makefile(mode='wb')
		dump(specs, outFlo)
		outFlo.flush()
		
		inFlo = sock.makefile(mode='rb')
		data = load(inFlo)
		sock.close()

		return True, data

	except Exception as e:
		success = False
		return False, str(e)
