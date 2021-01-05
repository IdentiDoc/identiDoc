import os
import sqlite3

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
            split_filename = filename.split(".", 1)
            assert len(split_filename) == 2

            self.timestamp = int(split_filename[0])
            self.filename = split_filename[1]
            self.classification = classification
            self.has_signature = int(has_signature)


        except AssertionError:
            self = None

    
    # Returns a tuple in the necessary form to insert a record into the database
    def to_tuple(self):
        return (self.timestamp, self.filename, self.classification, self.has_signature)


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
    # Make sure that the record is
    if record is None:
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
