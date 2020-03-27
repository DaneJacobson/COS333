#!/usr/bin/env python

#--------------------------------------------------------------------------------
# regserver_check.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from sys import argv, stderr, exit

#--------------------------------------------------------------------------------

def report_err(msg):
	print('regserver: '+msg, file=stderr)
	exit(1)

#--------------------------------------------------------------------------------

def check_len():
	if len(argv) != 2: report_err('Usage: python %s port' % argv[0])

#--------------------------------------------------------------------------------

def check_type():
	if not argv[1].isdigit(): report_err('port must be an integer')

#--------------------------------------------------------------------------------

def check_input():
	check_len()
	check_type()
	return int(argv[1])
