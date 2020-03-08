#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from reg_check import check_input
from reg_client import get_class_list, get_class_details
# from reg_gui import initialize_gui

def main():

	host, port = check_input()

	specs = {} # '-dept': , '-coursenum': , '-area': , '-title':

	success, data = get_class_list(host, port, specs)
	if success:
		for key, val in data.items():
			print(val)
		# initialize_gui(data)
	else:
		print('error:', data)

	classid = 8717
	success, data = get_class_details(host, port, classid)
	print(data)

#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()