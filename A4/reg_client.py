#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg_client.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from reg_check import report_err
from sys import argv, stderr
from threading import Thread
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
from pickle import load, dump
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QTimer

#-----------------------------------------------------------------------

class WorkerThread (Thread):

    def __init__(self, host, port, specs, queue):
        Thread.__init__(self)
        self._host = host
        self._port = port
        self._specs = specs
        self._queue = queue
        self._shouldStop = False
    
    def stop(self):
        self._shouldStop = True
        
    def run(self):   
        try:     
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((self._host, self._port))
            
            outFlo = sock.makefile(mode='wb')
            dump(self._specs, outFlo)
            outFlo.flush()
        
            inFlo = sock.makefile(mode='rb')
            data = load(inFlo)
            sock.close()

        except Exception as e:
            data = {'error': str(e)}
        
        if self._shouldStop:
            return

        self._queue.put(data)



def execute_client(host, port, specs):
	try:
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect((host, port))
		outFlo = sock.makefile(mode='wb')
		dump(specs, outFlo)
		outFlo.flush()
		
		inFlo = sock.makefile(mode='rb')
		data = load(inFlo)
		sock.close()

	except Exception as e:
		return False, str(e)

	if 'error' in data: return False, data['error']
	else: return True, data['success']

#--------------------------------------------------------------------------------

# returns success, errormsg or success, {...}
def get_class_list(host, port, specs):
	specs["type"] = 'list'
	execute_client(host, port, specs)

#--------------------------------------------------------------------------------

# returns success, errormsg or success, detailsstr
def get_class_details(host, port, classid):
	specs = {'classid': classid, 'type': 'details'}
	return execute_client(host, port, specs)
