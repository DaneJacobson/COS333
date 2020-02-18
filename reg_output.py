#!/usr/bin/env python

#-------------------------------------------------------------
# reg_output.py
# Author: Dane Jacobson and David Basili
#-------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect

#-------------------------------------------------------------

def IDcheck_conditionals(dictionary):
	c0, c1 = 0, 0
	if ('-dept' in dictionary or '-coursenum' in dictionary):
		c0 = 1
	if ('-area' in dictionary or '-title' in dictionary):
		c1 = 1
	return c0, c1

# SELECT classid, dept, coursenum, area, title FROM classes, courses, crosslistings WHERE classes.courseid = crosslistings.courseid AND classes.courseid = courses.courseid AND dept LIKE '%cos%' ORDER BY dept, coursenum, classid ASC;

# def add_IDchecks(dictionary, stmtStr):
# 	c0, c1 = IDcheck_conditionals(dictionary)

# 	if (c0 == 1 and c1 == 1):
# 		stmtStr += ' WHERE classes.courseid = crosslistings.courseid AND ' + \
# 				'classes.courseid = courses.courseid '
# 	elif (c0 == 1):
# 		stmtStr += ' WHERE classes.courseid = crosslistings.courseid'
# 	elif (c1 == 1):
# 		stmtStr += ' WHERE classes.courseid = courses.courseid'
# 	return stmtStr

def dept_String(dept):
	return " AND crosslistings.dept LIKE '%" + dept + "%'"

def coursenum_String(coursenum):
	return " AND crosslistings.coursenum LIKE '%" + coursenum + "%'"

def area_String(area):
	return " AND courses.area LIKE '%" + area + "%'"

def title_String(title):
	return " AND courses.title LIKE '%" + title + "%'"

def produce_output(dictionary):
	stmtStr = 'SELECT classid, dept, coursenum, area, title FROM classes, courses, crosslistings WHERE classes.courseid = crosslistings.courseid AND classes.courseid = courses.courseid'
	# stmtStr = add_IDchecks(dictionary, stmtStr)

	for key,value in dictionary.items():
		if (key == '-dept'):
			stmtStr += dept_String(value)
		elif (key == '-coursenum'):
			stmtStr += coursenum_String(value)
		elif (key == '-area'):
			stmtStr += area_String(value)
		elif (key == '-title'):
			stmtStr += title_String(value)

	stmtStr += ' ORDER BY dept, coursenum, classid ASC;'
	return stmtStr

def error_databaseconnection(DATABASE_NAME):
	if not path.isfile(DATABASE_NAME):
		raise Exception('Database connection failed')

def print_output(cursor):
	row = cursor.fetchone()
	while row is not None:
		print(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]) + '\t')
		row = cursor.fetchone()

def execute_output(dictionary, DATABASE_NAME):
	error_databaseconnection(DATABASE_NAME)

	connection = connect(DATABASE_NAME)
	cursor = connection.cursor()

	instruction = produce_output(dictionary)
	print(instruction)
	cursor.execute(instruction)
	print_output(cursor)

	cursor.close()
	connection.close()


	
