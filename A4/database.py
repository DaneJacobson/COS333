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
        self._database = 'reg.sqlite'

    def connect(self):      
        if path.isfile(self._database):
            self._connection = connect(self._database)
                    
    def disconnect(self):
        self._connection.close()

    def get_details(self, dictionary):
        self.connect()
        if self._connection is None: 
            print('database: database %s not found' % self._database, file=stderr)
            return {'error': 'database: database %s not found' % self._database}
        cursor = self._connection.cursor()
        info = db_details(cursor, dictionary)
        cursor.close()
        self.disconnect()
        return info

    def search(self, dictionary):
        self.connect()
        if self._connection is None: 
            print('database: database %s not found' % self._database, file=stderr)
            return {'error': 'database: database %s not found' % self._database}
        cursor = self._connection.cursor()
        info = db_search(cursor, dictionary)
        cursor.close()
        self.disconnect()
        return info

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    dictionary = {'classid':8361}
    dictionary_search = {'-dept':'cos'}
    info = database.get_details(dictionary)
    entries = database.search(dictionary_search)
    print(info)
    print(entries)
