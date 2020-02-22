#!/usr/bin/env python

#-------------------------------------------------------------
# reg_output.py
# Author: Dane Jacobson and David Basili
#-------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
from re import compile
from reg_check import report_err

#-------------------------------------------------------------

BEGINNING = 'SELECT classid, dept, coursenum, area, title FROM classes, courses, crosslistings ' + \
	'WHERE classes.courseid = crosslistings.courseid AND classes.courseid = courses.courseid'
DEPT = " AND crosslistings.dept LIKE ?"
CRS_NUM = " AND crosslistings.coursenum LIKE ?"
AREA = " AND courses.area LIKE ?"
TITLE = " AND courses.title LIKE ? ESCAPE '\\'"
ORDER = ' ORDER BY dept, coursenum, classid ASC;'

#--------------------------------------------------------------------------------

def make_connection(database):
	if not path.isfile(database):
		report_err("database reg.sqlite not found")
	connection = connect(database)
	cursor = connection.cursor()
	return connection, cursor

#--------------------------------------------------------------------------------

def produce_output(dictionary):
	stmtStr = BEGINNING
	vals = []
	for key,value in dictionary.items():
		value = value.replace('%', '\\%')
		value = value.replace('_', '\\_')
		value = value.lower()
		vals.append('%' + value + '%')
		if (key == '-dept'): stmtStr += DEPT
		elif (key == '-coursenum'): stmtStr += CRS_NUM
		elif (key == '-area'): stmtStr += AREA
		elif (key == '-title'): stmtStr += TITLE
	stmtStr += ORDER
	return stmtStr, vals

#--------------------------------------------------------------------------------

def get_title(title):
	CHARS_PER_LINE = 72 - 23

	result, outline = '', ''
	re_word = compile(r'\S+')
	words = re_word.findall(title)
	for word in words:
		if len(outline) + len(word) > CHARS_PER_LINE:
			result += outline.rstrip() + '\n                       '
			outline = ''
		outline += word + ' '
	if outline:
		result += outline.rstrip()
	return result

#--------------------------------------------------------------------------------

def print_h(cursor):
	print("ClsId Dept CrsNum Area Title")
	print("----- ---- ------ ---- -----")

	row = cursor.fetchone()
	while row is not None:
		classid, dept, crsnm = str(row[0]), str(row[1]), str(row[2])
		area = str(row[3])
		if (row[3] == ''): area = '  '
		title = get_title(row[4])
		print(' %s  %s    %s   %s %s' % (classid, dept, crsnm, area, title))
		row = cursor.fetchone()

#--------------------------------------------------------------------------------

def print_normal(cursor):
	row = cursor.fetchone()
	while row is not None:
		print(str(row[0]) + '\t' + str(row[1]) + '\t' + str(row[2]) + '\t' + str(row[3]) + '\t' + str(row[4]))
		row = cursor.fetchone()

#--------------------------------------------------------------------------------

def print_output(h, cursor):
	if h: print_h(cursor)
	else: print_normal(cursor)

#--------------------------------------------------------------------------------

def close(cursor, connection):
	cursor.close()
	connection.close()

#--------------------------------------------------------------------------------

def execute_output(dictionary, h, database):
	connection, cursor = make_connection(database)

	try:
		instruction, vals = produce_output(dictionary)
		cursor.execute(instruction, vals)
		print_output(h, cursor)
	except Exception as e:
		print('reg: ' + str(e), file=stderr)
		close(cursor, connection)
		exit(1)

	close(cursor, connection)



