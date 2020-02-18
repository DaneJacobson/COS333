#!/usr/bin/env python

#--------------------------------------------------------------------------------
# check_input.py
# Authors: David Basili
#--------------------------------------------------------------------------------

from sys import argv, stderr, exit

#--------------------------------------------------------------------------------

def report_err(msg):
	print(msg, file=stderr)
	exit(1)

#--------------------------------------------------------------------------------

def check_h(args, argv):
	if (len(argv) > 1 and argv[1] == '-h'): 
		args['-h'] = 'True'
		return 2
	return 1

#--------------------------------------------------------------------------------

def check_key(args, k):
	VALID_KEYS = ['-dept', '-coursenum', '-area', '-title']
	if k in args: report_err('reg: duplicate key')
	if not k in VALID_KEYS: report_err('reg: invalid key')

#--------------------------------------------------------------------------------

def check_value(argv, i):
	if (i >= len(argv)): report_err('reg: missing value')
	if (argv[i][0] == '-'): report_err('reg: missing value')

#--------------------------------------------------------------------------------

def check_input():
	args = {}
	start = check_h(args, argv)
	for i in range(start, len(argv), 2):
		check_key(args, argv[i])
		check_value(argv, i+1)
		args[argv[i]] = argv[i+1]
	return args




