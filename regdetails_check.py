#!/usr/bin/env python

#--------------------------------------------------------------------------------
# check_input.py
# Authors: David Basili
#--------------------------------------------------------------------------------

from sys import argv, stderr, exit

#--------------------------------------------------------------------------------

def report_err(msg):
	print('regdetails: ' + msg, file=stderr)
	exit(1)

#--------------------------------------------------------------------------------

def check_h(argv):
	return (len(argv) > 1 and argv[1] == '-h')

#--------------------------------------------------------------------------------

def check_classid(argv, h):
	loc = 2 if h else 1
	if len(argv) <= loc: report_err('missing classid')
	if not argv[loc].isdigit(): report_err('classid is not an integer')
	return loc

#--------------------------------------------------------------------------------

# check classid before length
def check_input():
	h = check_h(argv)
	loc = check_classid(argv, h)
	if len(argv) > loc+1: report_err('too many arguments')
	return argv[loc], h


