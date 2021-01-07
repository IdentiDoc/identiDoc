import unittest
import sqlite3

import identidoc.services.database


class TestDB(unittest.TestCase):
    def setUp(self):
        self.db_connection = sqlite3.connect(identidoc.services.database.identidoc_db)

        sql_create_table = """ CREATE TABLE IF NOT EXISTS classifications (
                               timestamp integer NOT NULL,
                               filename text NOT NULL,
                               classification integer NOT NULL,
                               has_signature integer NOT NULL,
                               PRIMARY KEY (timestamp, filename)
                           );"""
        
        c = self.db_connection.cursor()
        c.execute(sql_create_table)
        self.db_connection.commit()


    def tearDown(self):
        sql_delete_records = """ DELETE FROM classifications; """

        c = self.db_connection.cursor()
        c.execute(sql_delete_records)
        self.db_connection.commit()
        self.db_connection.close()
