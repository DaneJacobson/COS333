#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from regdetails_check import check_input
from regdetails_output import execute_output

def main():
	classid, h = check_input()
	execute_output(classid, h, 'reg.sqlite')


#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()