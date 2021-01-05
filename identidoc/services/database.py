import os
import sqlite3

# An object that is equivalent to a database record
#
# A list of ClassificaitonResultTableRows will be returned from a database query
# A ClassificationResultTableRow will need to be created to insert a database record
class ClassificationResultTableRow(object):
    # filename - raw filename from identidoc with timestamp
    # Example: 04122020164952378563.21-22_Verification_of_Household.pdf
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
            # which it should be. Please don't abuse this privileges
            split_filename = filename.split(".", 1)
            assert len(split_filename) == 2

            self.timestamp = split_filename[0]
            self.filename = split_filename[1]
            self.classification = classification
            self.has_signature = has_signature


        except AssertionError:
            self = None


# This function is run while creating the identiDoc program.
# Ensures that the .db file exists and can be connected to.
def validate_database():
    identidoc_db = os.environ.get('IDENTIDOC_DB', '')

    if identidoc_db == '':
        return -1

    conn = None

    try:
        conn = sqlite3.connect(identidoc_db)
        if create_table(conn) == -1:
            return -1
        conn.close()

    except:
        return -1
    
    return 0


# Helper function to create the db table needed for identidoc
def create_table(conn):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS classifications (
                               timestamp text PRIMARY KEY,
                               filename text NOT NULL,
                               classification integer NOT NULL,
                               has_signature integer NOT NULL
                           );"""

    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)
        return -1

    

    conn.commit()

    return 0

    
    