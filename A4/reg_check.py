#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg_check.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from sys import argv, stderr, exit

#--------------------------------------------------------------------------------

def report_err(msg):
	print('reg: '+msg, file=stderr)
	exit(1)

#--------------------------------------------------------------------------------

def check_len():
	if len(argv) != 3: report_err('Usage: python %s host port' % argv[0])

#--------------------------------------------------------------------------------

def check_type():
	if not argv[2].isdigit(): report_err('port must be an integer')

#--------------------------------------------------------------------------------

def check_input():
	check_len()
	check_type()
	return argv[1], int(argv[2])
