#!/usr/bin/env python

#-------------------------------------------------------------
# db_details.py
# Author: Dane Jacobson and David Basili
#-------------------------------------------------------------

from sys import stderr
from re import compile
#-------------------------------------------------------------

STR_LOC = 'SELECT courseid, days, starttime, endtime, bldg, roomnum FROM classes WHERE classid = ?;'
STR_DEPT = 'SELECT dept, coursenum FROM classes, crosslistings WHERE classes.courseid = crosslistings.courseid ' + \
			'AND classid = ? ORDER BY dept, coursenum ASC;'
STR_REQS = 'SELECT area, title, descrip, prereqs FROM classes, courses ' + \
			'WHERE classes.courseid = courses.courseid AND classid = ?;'
STR_PROF = 'SELECT profname FROM classes, coursesprofs, profs WHERE classes.courseid = coursesprofs.courseid ' + \
			'AND coursesprofs.profid = profs.profid AND classid = ? ORDER BY profname ASC;'

#--------------------------------------------------------------------------------

def call_db(cursor, instruction, classid):
	cursor.execute(instruction, [classid])
	row = cursor.fetchone()
	if row is None and instruction == STR_LOC: 
		raise Exception("classid does not exist")
	return row

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

def class_loc(cursor, classid):
	row = call_db(cursor, STR_LOC, classid)
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
	row = call_db(cursor, STR_DEPT, classid)
	result = ''
	while row is not None:
		result += msg.format(str(row[0]), str(row[1])) + '\n'
		row = cursor.fetchone()
	return result + '\n'

#--------------------------------------------------------------------------------

def crs_reqs(cursor, classid):
	row = call_db(cursor, STR_REQS, classid)
	s0, s1, s2, s3 = str(row[0]), str(row[1]), str(row[2]), str(row[3])
	s0 = 'Area: ' + s0 + '\n'
	s1 = norm('Title: ' + s1) + '\n'
	s2 = norm('Description: ' + s2) + '\n'
	s3 = norm('Prerequisites: ' + s3) + '\n'
	return '{}\n{}\n{}\n{}\n'.format(s0, s1, s2, s3)

#--------------------------------------------------------------------------------

def prof(cursor, classid):
	msg = 'Professor: {}'
	row = call_db(cursor, STR_PROF, classid)
	result = ''
	while row is not None:
		result += msg.format(str(row[0])) + '\n'
		row = cursor.fetchone()
	return result

#--------------------------------------------------------------------------------

def db_details(cursor, dictionary):
	try:
		classid = dictionary['classid']
		string = class_loc(cursor, classid)
		string += dept(cursor, classid)
		string += crs_reqs(cursor, classid)
		string += prof(cursor, classid)
		info = {'success': string}
	except Exception as e:
		print('database: ' + str(e), file=stderr)
		info = {'error': 'database: ' + str(e)}
	return info

