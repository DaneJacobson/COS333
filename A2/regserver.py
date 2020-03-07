#!/usr/bin/env python

#--------------------------------------------------------------------------------
# regserver.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from regserver_check import check_input
from regserver_server import execute_server

def main():

	port = check_input()
	execute_server(port)

#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()