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
from PyQt5.QtGui import QFont
from reg_client import get_class_list, get_class_details

#--------------------------------------------------------------------------------

class myListWidget(QListWidget):

	def __init__(self, host, port):
		super().__init__()
		self._host = host
		self._port = port

	def Activated(self, item, window):
		# splits text by space to retrieve classid and calls regdetails
		classid = item.text().split()[0]
		success, data = get_class_details(self._host, self._port, classid)
		# if successful print details, if not, print error message
		if success:
			QMessageBox.information(self, "Class Details", data)
		else:
			QMessageBox.information(self, "Database-Related Error", data)

	def update_dialogue(self, host, port, data):
		self.clear()
		i = 0
		for courseinfo in data:
			self.insertItem(i, courseinfo)
			i += 1

#--------------------------------------------------------------------------------

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
	widgets[5] = QLineEdit()	# dept_field
	widgets[6] = QLineEdit()	# number_field
	widgets[7] = QLineEdit()	# area_field
	widgets[8] = QLineEdit()	# title_field

	return widgets

#--------------------------------------------------------------------------------

def labelFrameLayout(widgets):
	labelFrameLayout = QGridLayout()
	labelFrameLayout.setSpacing(0)
	labelFrameLayout.setContentsMargins(0,0,0,0)
	labelFrameLayout.addWidget(widgets[1],0,0)	# dept_label
	labelFrameLayout.addWidget(widgets[2],1,0)	# number_label
	labelFrameLayout.addWidget(widgets[3],2,0)	# area_label
	labelFrameLayout.addWidget(widgets[4],3,0)	# title_label
	labelFrame = QFrame()
	labelFrame.setLayout(labelFrameLayout)

	return labelFrame

#--------------------------------------------------------------------------------

def fieldFrameLayout(widgets):
	fieldFrameLayout = QGridLayout()
	fieldFrameLayout.setSpacing(0)
	fieldFrameLayout.setContentsMargins(0,0,0,0)
	fieldFrameLayout.addWidget(widgets[5],0,0)	# dept_field
	fieldFrameLayout.addWidget(widgets[6],1,0)	# number_field
	fieldFrameLayout.addWidget(widgets[7],2,0)	# area_field
	fieldFrameLayout.addWidget(widgets[8],3,0)	# title_field
	fieldFrame = QFrame()
	fieldFrame.setLayout(fieldFrameLayout)

	return fieldFrame

#--------------------------------------------------------------------------------

def submitFrameLayout(widgets):
	submitFrameLayout = QGridLayout()
	submitFrameLayout.setSpacing(0)
	submitFrameLayout.setContentsMargins(0,0,0,0)
	submitFrameLayout.addWidget(widgets[0],0,0) # submit
	submitFrame = QFrame()
	submitFrame.setLayout(submitFrameLayout)

	return submitFrame

#--------------------------------------------------------------------------------

def inputFrameLayout(widgets):
	labelFrame = labelFrameLayout(widgets)
	fieldFrame = fieldFrameLayout(widgets)
	submitFrame = submitFrameLayout(widgets)
	inputFrameLayout = QGridLayout()
	inputFrameLayout.setSpacing(0)
	inputFrameLayout.setContentsMargins(0,0,0,0)
	inputFrameLayout.setRowStretch(0,0)
	inputFrameLayout.setColumnStretch(0,0)
	inputFrameLayout.setColumnStretch(1,1)
	inputFrameLayout.setColumnStretch(2,0)
	inputFrameLayout.addWidget(labelFrame,0,0)
	inputFrameLayout.addWidget(fieldFrame,0,1) 
	inputFrameLayout.addWidget(submitFrame,0,2)
	inputFrame = QFrame()
	inputFrame.setLayout(inputFrameLayout)
	
	return inputFrame

#--------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------

def window_gui(centralFrame):
	window = QMainWindow()
	window.setWindowTitle('Princeton University Class Search')
	window.setCentralWidget(centralFrame)
	screenSize = QDesktopWidget().screenGeometry()
	window.resize(screenSize.width()//2, screenSize.height()//2)
	
	return window

#--------------------------------------------------------------------------------

def initialize_framework(host, port, data):
	app = QApplication([])
	font = QFont("Courier")
	app.setFont(font)

	# sets up GUI framework
	widgets = design_gui()
	inputFrame = inputFrameLayout(widgets)
	dialogue = myListWidget(host, port)
	dialogue.update_dialogue(host, port, data)
	dialogueFrame = dialogueFrameLayout(data, dialogue)
	centralFrame = centralFrameLayout(inputFrame, dialogueFrame)
	window = window_gui(centralFrame)

	return app, widgets, dialogue, window

#--------------------------------------------------------------------------------

def signal_setup(host, port, widgets, dialogue, window):

	def submitButtonSlot():
		# creates request dictionary for server query
		request = {}
		if not widgets[5].text() == '': request['-dept'] = widgets[5].text()
		if not widgets[6].text() == '': request['-coursenum'] = widgets[6].text()
		if not widgets[7].text() == '': request['-area'] = widgets[7].text()
		if not widgets[8].text() == '': request['-title'] = widgets[8].text()

		# queries database and prints class details or error message
		success, data = get_class_list(host, port, request)	
		if success:
			dialogue.update_dialogue(host, port, data)
		else:
			QMessageBox.information(window, "Database-Related Error", data)

	widgets[0].clicked.connect(submitButtonSlot)
	widgets[5].returnPressed.connect(submitButtonSlot)
	widgets[6].returnPressed.connect(submitButtonSlot)
	widgets[7].returnPressed.connect(submitButtonSlot)
	widgets[8].returnPressed.connect(submitButtonSlot)
	dialogue.itemActivated.connect(dialogue.Activated)

#--------------------------------------------------------------------------------

def initialize_gui(host, port, data):
	# GUI framework initialization
	app, widgets, dialogue, window = initialize_framework(host, port, data)

	# signals for GUI functionality
	signal_setup(host, port, widgets, dialogue, window)

	# epilogue
	window.show()
	exit(app.exec_())
