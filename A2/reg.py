#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from reg_check import check_input
from reg_client import execute_client

def main():

	host, port = check_input()

	specs = {'-dept': 'cos', '-title': 'cs'} # '-dept': , '-coursenum': , '-area': , '-title':}
	success, data = execute_client(host, port, specs)

	if success:
		for key, val in data.items():
			print(val)
	else:
		print('reg: ' + data)

#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()