#!/usr/bin/env python

#--------------------------------------------------------------------------------
# reg_gui.py
# Authors: David Basili, Dane Jacobson
#--------------------------------------------------------------------------------

from sys import exit
from PyQt5.QtWidgets import QApplication, QFrame, QLabel
from PyQt5.QtWidgets import QMainWindow, QGridLayout, QDesktopWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QListWidget
from PyQt5.QtCore import Qt

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
	inputFrameLayout.addWidget(widgets[0],1,2)
	inputFrameLayout.addWidget(widgets[1],0,0)
	inputFrameLayout.addWidget(widgets[2],1,0)
	inputFrameLayout.addWidget(widgets[3],2,0)
	inputFrameLayout.addWidget(widgets[4],3,0)
	inputFrameLayout.addWidget(widgets[5],0,1)
	inputFrameLayout.addWidget(widgets[6],1,1)
	inputFrameLayout.addWidget(widgets[7],2,1)
	inputFrameLayout.addWidget(widgets[8],3,1)
	inputFrame = QFrame()
	inputFrame.setLayout(inputFrameLayout)
	return inputFrame

def dialogueFrameLayout():

	success, data = execute_client


	dialogue = QListWidget()
	dialogue.insertItem(0, 'sup')
	dialogue.insertItem(1, 'David')
	dialogue.insertItem(2, 'you')
	dialogue.insertItem(3, 'suck')
	dialogue.insertItem(4, 'a lot')

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

def main():
	app = QApplication([])

	widgets = design_gui()
	inputFrame = inputFrameLayout(widgets)

	dialogueFrame = dialogueFrameLayout()

	centralFrame = centralFrameLayout(inputFrame, dialogueFrame)

	window = window_gui(centralFrame)

	window.show()
	exit(app.exec_())

if __name__ == '__main__':
	main()
