#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg_gui.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from sys import exit
from PyQt5.QtWidgets import QApplication, QFrame, QLabel
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QListWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt
from reg_client import get_class_list, get_class_details


def design_gui():
	widgets = [None] * 9
	widgets[0] = QPushButton('Submit')
	widgets[1] = QLabel('Dept:')
	widgets[1].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
	widgets[2] = QLabel('Number:')
	widgets[2].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
	widgets[3] = QLabel('Area:')
	widgets[3].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
	widgets[4] = QLabel('Title:')
	widgets[4].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
	widgets[5] = QLineEdit()
	widgets[6] = QLineEdit()
	widgets[7] = QLineEdit()
	widgets[8] = QLineEdit()

	return widgets

def inputFrameLayout(widgets):
	inputFrameLayout = QGridLayout()
	inputFrameLayout.setSpacing(0)
	inputFrameLayout.setContentsMargins(0,0,0,0)
	inputFrameLayout.setRowStretch(0,0)
	inputFrameLayout.setRowStretch(1,0)
	inputFrameLayout.setRowStretch(2,0)
	inputFrameLayout.setRowStretch(3,0)
	inputFrameLayout.setColumnStretch(0,0)
	inputFrameLayout.setColumnStretch(1,1)
	inputFrameLayout.setColumnStretch(2,0)
	inputFrameLayout.addWidget(widgets[0],1,2) # submit
	inputFrameLayout.addWidget(widgets[1],0,0) # dept label
	inputFrameLayout.addWidget(widgets[2],1,0) # number label
	inputFrameLayout.addWidget(widgets[3],2,0) # area label
	inputFrameLayout.addWidget(widgets[4],3,0) # title label
	inputFrameLayout.addWidget(widgets[5],0,1) # dept field
	inputFrameLayout.addWidget(widgets[6],1,1) # number field
	inputFrameLayout.addWidget(widgets[7],2,1) # area field
	inputFrameLayout.addWidget(widgets[8],3,1) # title field
	inputFrame = QFrame()
	inputFrame.setLayout(inputFrameLayout)
	
	return inputFrame

def dialogueFrameLayout(data, dialogue):

	dialogueFrameLayout = QGridLayout()
	dialogueFrameLayout.setSpacing(0)
	dialogueFrameLayout.setContentsMargins(0,0,0,0)
	dialogueFrameLayout.setRowStretch(0,0)
	dialogueFrameLayout.setColumnStretch(0,0)
	dialogueFrameLayout.addWidget(dialogue,0,0)
	dialogueFrame = QFrame()
	dialogueFrame.setLayout(dialogueFrameLayout)
	
	return dialogueFrame

def centralFrameLayout(inputFrame, dialogueFrame):
	centralFrameLayout = QGridLayout()
	centralFrameLayout.setSpacing(0)
	centralFrameLayout.setContentsMargins(0,0,0,0)
	centralFrameLayout.setRowStretch(0,0)
	centralFrameLayout.setRowStretch(1,1)
	centralFrameLayout.setColumnStretch(0,1)
	centralFrameLayout.addWidget(inputFrame,0,0)
	centralFrameLayout.addWidget(dialogueFrame,1,0)
	centralFrame = QFrame()
	centralFrame.setLayout(centralFrameLayout)
	
	return centralFrame

def window_gui(centralFrame):
	window = QMainWindow()
	window.setWindowTitle('Princeton University Class Search')
	window.setCentralWidget(centralFrame)
	screenSize = QDesktopWidget().screenGeometry()
	window.resize(screenSize.width()//2, screenSize.height()//2)
	
	return window

class myListWidget(QListWidget):

	def __init__(self, host, port, data):
		super().__init__()
		self._host = host
		self._port = port
		i = 0
		for courseinfo in data:
			self.insertItem(i, courseinfo)
			i += 1

	def Clicked(self, item):
		classid = item.text().split()[0]
		success, data = get_class_details(self._host, self._port, classid)
		if success:
			QMessageBox.information(self, "ListWidget", data)

	def update_dialogue(self, data):
		i = 0
		for courseinfo in data:
			self._dialogue.insertItem(i, courseinfo)
			i += 1
		self.itemDoubleClicked.connect(dialogue.Clicked)
		self.repaint()

def initialize_gui(host, port, data):
	app = QApplication([])

	widgets = design_gui()
	inputFrame = inputFrameLayout(widgets)

	dialogue = myListWidget(host, port, data)

	dialogueFrame = dialogueFrameLayout(data, dialogue)

	centralFrame = centralFrameLayout(inputFrame, dialogueFrame)

	window = window_gui(centralFrame)

	def submitButtonSlot():
		request = {}
		if not widgets[5].text() == '': request['-dept'] = widgets[5].text()
		if not widgets[6].text() == '': request['-coursenum'] = widgets[6].text()
		if not widgets[7].text() == '': request['-area'] = widgets[7].text()
		if not widgets[8].text() == '': request['-title'] = widgets[8].text()

		for thing in request.items():
			print(thing)

		success, data = get_class_list(host, port, request)	
		print(data)
		if success:
			dialogue = update_dialogue(host, port, data)
			dialogue.repaint()

	widgets[0].clicked.connect(submitButtonSlot)

	window.show()
	exit(app.exec_())
