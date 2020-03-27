#!/usr/bin/env python

#-----------------------------------------------------------------------
# database_regdetails.py
# Author: David Basili and Dane Jacobson
#-----------------------------------------------------------------------

from os import path
from sys import stderr
from sqlite3 import connect
from db_details import db_details
from db_search import db_search
#-------------------------------------------------------------

class Database:
    
    def __init__(self):
        self._connection = None

    def connect(self):      
        DATABASE_NAME = 'reg.sqlite'
        if path.isfile(DATABASE_NAME):
            self._connection = connect(DATABASE_NAME)
                    
    def disconnect(self):
        self._connection.close()

    def get_details(self, dictionary):
        self.connect()
        if self._connection is None: 
            print('database: database %s not found' % DATABASE, file=stderr)
            return {'error': 'database: database %s not found' % DATABASE}
        cursor = self._connection.cursor()
        info = db_details(cursor, dictionary)
        cursor.close()
        self.disconnect()
        return info

    def search(self, dictionary):
        self.connect()
        if self._connection is None: 
            print('database: database %s not found' % DATABASE, file=stderr)
            return {'error': 'database: database %s not found' % DATABASE}
        cursor = self._connection.cursor()
        info = db_search(cursor, dictionary)
        cursor.close()
        self.disconnect()
        return info

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    dictionary = {'classid':9980}
    dictionary_search = {'-dept':'cos'}
    info = database.get_details(dictionary)
    entries = database.search(dictionary_search)
    formatted_txt = []
    for entry in entries['success']:
        formatted_txt.append('{:>5}{:>5}{:>7}{:>5} {}'.format(entry['classid'], entry['dept'], entry['coursenum'], entry['area'], entry['title']))
    for txt in formatted_txt:
        print(txt)
