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

		if "error" in data: return False, data["error"]
		return True, data

	except Exception as e:
		return False, str(e)


#--------------------------------------------------------------------------------

# returns {'error': errormsg} or {...}
def get_class_list(host, port, specs):
	specs["type"] = 'list'
	return execute_client(host, port, specs)

#--------------------------------------------------------------------------------

# returns errormsg or detailsstr
def get_class_details(host, port, classid):
	specs = {'classid': classid, 'type': 'details'}
	success, msg = execute_client(host, port, specs)
	if success: return True, msg['success']
	else: return False, msg
