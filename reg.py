#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from check_input import check_input
from reg_output import execute_output

def main():

	inputs, h = check_input()
	execute_output(inputs, h, 'reg.sqlite')


#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()