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

	except Exception as e:
		return False, str(e)

	if 'error' in data: return False, data['error']
	else: return True, data['success']

#--------------------------------------------------------------------------------

# returns success, errormsg or success, {...}
def get_class_list(host, port, specs):
	specs["type"] = 'list'
	return execute_client(host, port, specs)

#--------------------------------------------------------------------------------

# returns success, errormsg or success, detailsstr
def get_class_details(host, port, classid):
	specs = {'classid': classid, 'type': 'details'}
	return execute_client(host, port, specs)
