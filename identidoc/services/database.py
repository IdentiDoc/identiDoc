import os
import sqlite3
import pytz

from datetime import datetime, timedelta, timezone
from typing import List

import identidoc.services

# An object that is equivalent to a database record
#
# A list of ClassificaitonResultTableRows will be returned from a database query
# A ClassificationResultTableRow will need to be created to insert a database record
class ClassificationResultTableRow(object):
    # filename - raw filename from identidoc with POSIX timestamp
    # Example: 1609865062.Class3-2.pdf
    #
    # classification - an integer 0 - 5 inclusive
    # 1 - 5 is a classified document
    # 0 is a non-classified document
    # 
    # has_signature - True or False
    #
    # After constructing an object, ensure that it is not None
    def __init__(self, filename, classification, has_signature):
        try:
            # Ensure that the classification field is an integer and falls within the acceptable interval
            assert isinstance(classification, int)
            assert 0 <= classification and classification <= 5

            assert isinstance(has_signature, bool)

            # We're going to assume that the filename has already been validated/created through the api,
            # which it should be. Please don't abuse this privilege
            assert isinstance(filename, str)
            split_filename = filename.split(".", 1)

            self.timestamp = int(split_filename[0])
            self.filename = split_filename[1]
            self.classification = classification
            self.has_signature = int(has_signature)
            self.is_invalid = False


        except AssertionError:
            self.is_invalid = True

    
    # Returns a tuple in the necessary form to insert a record into the database
    def to_tuple(self):
        if self.is_invalid:
            return None

        return (self.timestamp, self.filename, self.classification, self.has_signature)


# This object will handle the query including validation.
# By design, this object should not be accessed outside of this file
class ClassificationResultQuery(object):
    def __init__(self, classification_date, classification, has_signature):
        try:
            if classification_date is not None:
                assert isinstance(classification_date, datetime)

            if classification is not None:
                assert isinstance(classification, int)
                assert 0 <= classification and classification <= 5
            
            if has_signature is not None:
                assert isinstance(has_signature, bool)

            self.classification_date = classification_date
            self.classification = classification
            self.has_signature = has_signature
            self.is_invalid = False
        
        except AssertionError:
            self.is_invalid = True

    # returns two POSIX time stamps for the query
    # The first represents the first second of the
    # indicated date, the second represents the last
    # second of the indicated date
    def generate_date_range(self):
        if self.is_invalid:
            return None

        orig_date = self.classification_date

        # Just get the day month and year of the date passed in, don't rely on the time being midnight
        day = orig_date.day
        month = orig_date.month
        year = orig_date.year

        central = pytz.timezone('US/Central')

        # Assume that the datetime object passed in is in Central Time
        start_date = central.localize(datetime(year=year,
                                               month=month,
                                               day=day,
                                               hour=0,
                                               minute=0,
                                               second=0,
                                               microsecond=0))

        start_date = start_date.astimezone(pytz.timezone('UTC'))
        end_date = start_date + timedelta(days=1)

        start_date_timestamp = identidoc.services.datetime_to_POSIX_timestamp(start_date)
        end_date_timestamp = identidoc.services.datetime_to_POSIX_timestamp(end_date)

        return [start_date_timestamp, end_date_timestamp]


    # Member function to generate the query string necessary.
    # All members of the object were validated in the constructor
    def generate_query_string(self):
        if self.is_invalid:
            return None
        
        query_string = 'SELECT * FROM classifications'

        previous_clause = False

        if self.classification_date is not None:
            date_range = self.generate_date_range()

            query_string += ' WHERE ' + str(date_range[0]) + ' <= timestamp AND timestamp < ' + str(date_range[1])

            previous_clause = True

        
        if self.classification is not None:
            if previous_clause:
                query_string += ' AND '
            else:
                query_string += ' WHERE '
            
            query_string += 'classification = ' + str(self.classification)

            previous_clause = True

        
        if self.has_signature is not None:
            if previous_clause:
                query_string += ' AND '
            else:
                query_string += ' WHERE '

            value = 0
            if self.has_signature:
                value = 1

            query_string += 'has_signature = ' + str(value)


        return query_string + ';'
            
# The result of the query.
# Records retrieved from the database are represented by this object
#
# Since results are coming from the database, no validation is necessary
#
# self.timestamp is a POSIX timestamp. This value will be sent to the frontend
# and needs to be handled there to disply it to the user in a pretty way
# self.filename is the filename without the timestamp
# self.classification is an integer with the class
# self.has_signature is either a 0 or a 1 (0 is false, 1 is true). This is an integer
class QueryResultRow(object):
    def __init__(self, record_tuple):
        self.timestamp = record_tuple[0]
        self.filename = record_tuple[1]
        self.classification = record_tuple[2]
        self.has_signature = record_tuple[3]


# The location of the identidoc database - env variable
identidoc_db = os.environ.get('IDENTIDOC_DB', '')


# This function is run while creating the identiDoc program.
# Ensures that the .db file exists and can be connected to.
def validate_database():
    if identidoc_db == '':
        return -1

    conn = None

    try:
        conn = sqlite3.connect(identidoc_db)

        if create_table(conn) == -1:
            conn.close()
            return -1

        conn.close()

    except:
        return -1
    
    return 0


# Helper function to create the db table needed for identidoc
def create_table(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS classifications (
                               timestamp integer NOT NULL,
                               filename text NOT NULL,
                               classification integer NOT NULL,
                               has_signature integer NOT NULL,
                               PRIMARY KEY (timestamp, filename)
                           );"""

    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    
    # Something went wrong, rollback the transaction
    except sqlite3.Error:
        conn.rollback()
        return -1    

    conn.commit()

    return 0

    
# Inserts a record into the database
# This function should be the only way to insert a record into the database.
# Only one record can be inserted at a time since only one file can be classified at a time
# This command does not return any data from the database to honor CQS (command-query separation)
#
# This function returns -1 on any failure and 0 on success
def insert_record_command(record: ClassificationResultTableRow) -> int:
    # Make sure that the record is valid
    if record.is_invalid:
        return -1

    try:
        conn = sqlite3.connect(identidoc_db)
        c = conn.cursor()
        c.execute('INSERT INTO classifications VALUES ?;', record.to_tuple())
    
    except sqlite3.Error:
        conn.rollback()
        conn.close()
        return -1

    conn.commit()
    conn.close()

    return 0


# This is a generic function to execute the database query to retrieve the records
# It is assumed that the user will be able to filter by the document's classification date,
# classification, and whether or not a signiture is present.
#
# classification_date: datetime object representing the date - IT IS ASSUMED THAT THIS DATE IS IN CENTRAL TIME ***NOT*** UTC
# classification: the class of the document in question
# has_signature: bool value of whether or not a signature is present
#
# This function will return an empty list on error. NO ERROR MESSAGE WILL BE GIVEN FOR SECURITY PURPOSES
# On a non-error, this function will return a list of zero or more QueryResultRows
def retrieve_records_query(classification_date: datetime, classification: int, has_signature: bool) -> List[QueryResultRow]:
    Query = ClassificationResultQuery(classification_date, classification, has_signature)

    if Query.is_invalid:
        return []

    query_string = Query.generate_query_string()

    try:
        conn = sqlite3.connect(identidoc_db)
        c = conn.cursor()
        c.execute(query_string)
    
    except sqlite3.Error:
        conn.close()
        return []

    query_results = c.fetchall()

    query_result_list = []

    for record_tuple in query_results:
        query_result_list.append(QueryResultRow(record_tuple))

    return query_results
