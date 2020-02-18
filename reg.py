#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from check_input import check_input
from reg_output import execute_output

def main():
	inputs = check_input()
	print(inputs)
	execute_output(inputs, 'reg.sqlite')


#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()