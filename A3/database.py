#!/usr/bin/env python

#-----------------------------------------------------------------------
# database_regdetails.py
# Author: David Basili and Dane Jacobson
#-----------------------------------------------------------------------

from os import path
from sys import stderr
from sqlite3 import connect
from db_details import get_details
from db_search import search
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
        connect()
        if self._connection is None: 
            print('database: database %s not found' % DATABASE, file=stderr)
            return {'error': 'database: database %s not found' % DATABASE}
        cursor = self._connection.cursor()
        info = fetch_details(cursor, dictionary)
        cursor.close()
        disconnect()
        return info

    def search(self, dictionary):
        connect()
        if self._connection is None: 
            print('database: database %s not found' % DATABASE, file=stderr)
            return {'error': 'database: database %s not found' % DATABASE}
        cursor = self._connection.cursor()
        info = search(cursor, dictionary)
        cursor.close()
        disconnect()
        return info

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    info = database.search({})
    print(info)
