#!/usr/bin/env python

#-------------------------------------------------------------
# regserver_regdetails_db.py
# Author: Dane Jacobson and David Basili
#-------------------------------------------------------------

from os import path
from sys import argv, stderr, exit
from sqlite3 import connect
from re import compile
#-------------------------------------------------------------

CLASS_LOC = 'SELECT courseid, days, starttime, endtime, bldg, roomnum FROM classes WHERE classid = ?;'
DEPT = 'SELECT dept, coursenum FROM classes, crosslistings WHERE classes.courseid = crosslistings.courseid ' + \
'AND classid = ? ORDER BY dept, coursenum ASC;'
CRS_REQS = 'SELECT area, title, descrip, prereqs FROM classes, courses ' + \
'WHERE classes.courseid = courses.courseid AND classid = ?;'
PROF = 'SELECT profname FROM classes, coursesprofs, profs WHERE classes.courseid = coursesprofs.courseid ' + \
'AND coursesprofs.profid = profs.profid AND classid = ? ORDER BY profname ASC;'

#--------------------------------------------------------------------------------

def make_connection(database):
	if not path.isfile(database):
		return True, None, None
	connection = connect(database)
	cursor = connection.cursor()
	return False, connection, cursor

#--------------------------------------------------------------------------------

def norm(line):
	CHARS_PER_LINE = 72

	result, outline = '', ''
	re_word = compile(r'\S+')
	words = re_word.findall(line)
	for word in words:
		if len(outline) + len(word) > CHARS_PER_LINE:
			result += outline.rstrip() + '\n'
			outline = ''
		outline += word + ' '
	if outline:
		result += outline.rstrip()
	return result

#--------------------------------------------------------------------------------

def call_db(cursor, instruction, classid):
	cursor.execute(instruction, [classid])
	row = cursor.fetchone()
	if row is None and instruction == CLASS_LOC:
		raise Exception("classid does not exist")
	return row

#--------------------------------------------------------------------------------

def class_loc(cursor, classid):
	row = call_db(cursor, CLASS_LOC, classid)
	s0, s1, s2, s3, s4, s5 = str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5])
	s0 = 'Course Id: ' + s0 + '\n'
	s1 = 'Days: ' + s1
	s2 = 'Start time: ' + s2
	s3 = 'End time: ' + s3
	s4 = 'Building: ' + s4
	s5 = 'Room: ' + s5 + '\n'
	return '{}\n{}\n{}\n{}\n{}\n{}\n'.format(s0, s1, s2, s3, s4, s5)

#--------------------------------------------------------------------------------

def dept(cursor, classid):
	msg = 'Dept and Number: {} {}'
	row = call_db(cursor, DEPT, classid)
	result = ''
	while row is not None:
		result += msg.format(str(row[0]), str(row[1])) + '\n'
		row = cursor.fetchone()
	return result + '\n'

#--------------------------------------------------------------------------------

def crs_reqs(cursor, classid):
	row = call_db(cursor, CRS_REQS, classid)
	s0, s1, s2, s3 = str(row[0]), str(row[1]), str(row[2]), str(row[3])
	s0 = 'Area: ' + s0 + '\n'
	s1 = norm('Title: ' + s1) + '\n'
	s2 = norm('Description: ' + s2) + '\n'
	s3 = norm('Prerequisites: ' + s3) + '\n'
	return '{}\n{}\n{}\n{}\n'.format(s0, s1, s2, s3)

#--------------------------------------------------------------------------------

def prof(cursor, classid):
	msg = 'Professor: {}'
	row = call_db(cursor, PROF, classid)
	result = ''
	while row is not None:
		result += msg.format(str(row[0])) + '\n'
		row = cursor.fetchone()
	return result

#--------------------------------------------------------------------------------

def close(cursor, connection):
	cursor.close()
	connection.close()

#--------------------------------------------------------------------------------

def access_regdetails_db(dictionary):
	DATABASE = 'reg.sqlite'
	error, connection, cursor = make_connection(DATABASE)
	if error: 
		print('regserver: database %s not found' % DATABASE, file=stderr)
		return {'error': 'regserver: database %s not found' % DATABASE}
	classid = dictionary['classid']

	try:
		string = class_loc(cursor, classid)
		string += dept(cursor, classid)
		string += crs_reqs(cursor, classid)
		string += prof(cursor, classid)
	except Exception as e:
		print('regserver: ' + str(e), file=stderr)
		close(cursor, connection)
		return {'error': 'regserver: ' + str(e)}

	close(cursor, connection)
	return {'success': string}




	
