#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from reg_check import check_input
from reg_client import get_class_list, get_class_details
from reg_gui import initialize_gui
from PyQt5.QtWidgets import QMessageBox

def main():

	host, port = check_input()

	specs = {} # '-dept': , '-coursenum': , '-area': , '-title':

	success, data = get_class_list(host, port, specs)
	if success:
		initialize_gui(host, port, data)
	else:
		print(data, file=stderr)

#--------------------------------------------------------------------------------

if __name__ == '__main__':
	main()