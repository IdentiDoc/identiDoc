# BE WARNED, DO NOT RUN THIS TEST IF YOU VALUE YOUR IDENTIDOC DATABASE, RECORDS WILL BE ERASED, BACK IT UP SOMEWHERE FIRST

import unittest
import sqlite3
import json

from datetime import datetime

from identidoc.services.database import ClassificationResultTableRow, ClassificationResultQuery, QueryResultRow, insert_record_command, retrieve_records_query, validate_database, identidoc_db

class TestDB(unittest.TestCase):
    # Ensure that the database exists with the correct table
    # Make sure no records are in the database before the unittest
    def setUp(self):
        validate_database()
    

    # This test will check the validation of the ClassificationResultTableRow
    # In the constructor, if the arguements are invalid, a None object is returned
    def test_ClassificationResultTableRow_constructor(self):
        # All arguemnents of ClassificationResultTableRow must not be None
        no_filename = ClassificationResultTableRow(None, 0, False)
        no_classification = ClassificationResultTableRow('1609865062.Class3-2.pdf', None, False)
        no_signature = ClassificationResultTableRow('1609865062.Class3-2.pdf', 0, None)

        assert no_filename.is_invalid
        assert no_classification.is_invalid
        assert no_signature.is_invalid

        # The filename should be and is assumed to be generated by identiDoc, so no real validation on it

        # Classification must be an int between 0 and 5 inclusive
        classification_wrong_datatype_1 = ClassificationResultTableRow('1610121696.file.png', ['list', 'for', 'some', 'reason'], True)
        classification_wrong_datatype_2 = ClassificationResultTableRow('1610121696.file.png', 'classification', True)
        classification_wrong_datatype_3 = ClassificationResultTableRow('1610121696.file.png', 2.1, True)

        assert classification_wrong_datatype_1.is_invalid
        assert classification_wrong_datatype_2.is_invalid
        assert classification_wrong_datatype_3.is_invalid

        # Correct data type and valid values
        classification_correct_datatype_0 = ClassificationResultTableRow('1610121696.file.png', 0, False)
        classification_correct_datatype_1 = ClassificationResultTableRow('1610121696.file.png', 1, False)
        classification_correct_datatype_2 = ClassificationResultTableRow('1610121696.file.png', 2, False)
        classification_correct_datatype_3 = ClassificationResultTableRow('1610121696.file.png', 3, False)
        classification_correct_datatype_4 = ClassificationResultTableRow('1610121696.file.png', 4, False)
        classification_correct_datatype_5 = ClassificationResultTableRow('1610121696.file.png', 5, False)

        assert not classification_correct_datatype_0.is_invalid
        assert not classification_correct_datatype_1.is_invalid
        assert not classification_correct_datatype_2.is_invalid
        assert not classification_correct_datatype_3.is_invalid
        assert not classification_correct_datatype_4.is_invalid
        assert not classification_correct_datatype_5.is_invalid

        classification_outside_range_1 = ClassificationResultTableRow('1610121696.file.png', -1, True)
        classification_outside_range_2 = ClassificationResultTableRow('1610121696.file.png', 6, True)
        classification_outside_range_3 = ClassificationResultTableRow('1610121696.file.png', 25, True)
        classification_outside_range_4 = ClassificationResultTableRow('1610121696.file.png', -1000, True)

        assert classification_outside_range_1.is_invalid
        assert classification_outside_range_2.is_invalid
        assert classification_outside_range_3.is_invalid
        assert classification_outside_range_4.is_invalid

        signature_wrong_datatype_1 = ClassificationResultTableRow('1610121696.file.pdf', 2, 1)
        signature_wrong_datatype_2 = ClassificationResultTableRow('1610121696.file.pdf', 2, [])
        signature_wrong_datatype_3 = ClassificationResultTableRow('1610121696.file.pdf', 2, 'True')
        signature_wrong_datatype_4 = ClassificationResultTableRow('1610121696.file.pdf', 2, 2.3)

        assert signature_wrong_datatype_1.is_invalid
        assert signature_wrong_datatype_2.is_invalid
        assert signature_wrong_datatype_3.is_invalid
        assert signature_wrong_datatype_4.is_invalid

        signature_correct_datatype_1 = ClassificationResultTableRow('1610122596.doc.png', 2, True)
        signature_correct_datatype_2 = ClassificationResultTableRow('1610122596.doc.png', 2, False)

        assert not signature_correct_datatype_1.is_invalid
        assert not signature_correct_datatype_2.is_invalid


    # This function creates a tuple for insertion into the database
    def test_ClassificationResultTableRow_tuple_generator(self):
        invalid_obj = ClassificationResultTableRow('1610121696.file.png', ['list', 'for', 'some', 'reason'], True)

        assert invalid_obj.to_tuple() is None

        valid_obj_1 = ClassificationResultTableRow('1610121696.file.png', 0, False)
        valid_obj_2 = ClassificationResultTableRow('1610121696.this.is.a.valid.filename.pdf', 1, False)
        valid_obj_3 = ClassificationResultTableRow('1610124814.file.png', 2, True)

        assert valid_obj_1.to_tuple() == (1610121696, 'file.png', 0, False)
        assert valid_obj_2.to_tuple() == (1610121696, 'this.is.a.valid.filename.pdf', 1, False)
        assert valid_obj_3.to_tuple() == (1610124814, 'file.png', 2, True)

    
    # Test Query Validation
    def test_ClassificationResultQuery_constructor(self):
        datetime_one = datetime.now()
        datetime_two = datetime(2021, 1, 1, 0, 0, 0, 0)
        datetime_three = datetime(2021, 5, 15, 12, 0, 0, 0)

        # The query object doesn't have to have all fields filled in
        no_date = ClassificationResultQuery(None, 3, True)
        no_classification = ClassificationResultQuery(datetime_one, None, False)
        no_signature = ClassificationResultQuery(datetime_two, 0, None)
        no_constraints = ClassificationResultQuery(None, None, None)

        assert not no_date.is_invalid
        assert not no_classification.is_invalid
        assert not no_signature.is_invalid
        assert not no_constraints.is_invalid

        wrong_data_type_1 = ClassificationResultQuery(2, 1, True)
        wrong_data_type_2 = ClassificationResultQuery(datetime_three, '3', False)
        wrong_data_type_3 = ClassificationResultQuery(datetime_one, 2, 'True')

        assert wrong_data_type_1.is_invalid
        assert wrong_data_type_2.is_invalid
        assert wrong_data_type_3.is_invalid

        out_of_class_range_1 = ClassificationResultQuery(datetime_one, -1, True)
        out_of_class_range_2 = ClassificationResultQuery(datetime_one, 6, True)
        out_of_class_range_3 = ClassificationResultQuery(datetime_one, 27, True)
        out_of_class_range_4 = ClassificationResultQuery(datetime_one, -14165, True)

        assert out_of_class_range_1.is_invalid
        assert out_of_class_range_2.is_invalid
        assert out_of_class_range_3.is_invalid
        assert out_of_class_range_4.is_invalid


        valid_query_1 = ClassificationResultQuery(datetime_one, 5, True)
        valid_query_2 = ClassificationResultQuery(datetime_two, 2, False)
        valid_query_3 = ClassificationResultQuery(datetime_three, 0, True)

        assert not valid_query_1.is_invalid
        assert not valid_query_2.is_invalid
        assert not valid_query_3.is_invalid

    
    # Test that the date range conversion is working correctly. This is a little tricky
    # A date is passed in (Assume this date is in Central time)
    # A list of two integers (POSIX timestamps) is returned.
    # The first timestamp represents midnight (CST) of the day passed in
    # The second timestamp represents midnight (CST) of the next day
    # NOTE - POSIX timestamps are in UTC and this must be handled appropriately
    def test_ClassificationResultQuery_generate_date_range(self):
        day_one = datetime(2020, 9, 21)     # Daylight Savings
        day_two = datetime(2020, 11, 22)    # No Daylight Savings
        day_thee = datetime(2020, 12, 31)   # This testcase will require rollover for day, month and year

        # This query is invalid and will return None when generate_date_range() is called
        invalid_query = ClassificationResultQuery(day_two, '3', True)
        assert invalid_query.generate_date_range() == None

        query_1 = ClassificationResultQuery(day_one, 3, True)
        query_2 = ClassificationResultQuery(day_two, 0, False)
        query_3 = ClassificationResultQuery(day_thee, 4, False)

        # Values generated using online Epoch calculator.
        # MIDNIGHT CST
        assert query_1.generate_date_range() == [1600664400, 1600750800]
        assert query_2.generate_date_range() == [1606024800, 1606111200]
        assert query_3.generate_date_range() == [1609394400, 1609480800]

    
    # Ensure that expected query strings are being generated
    def test_ClassificationResultQuery_query_string_generator(self):
        day_one = datetime(2020, 9, 21)
        day_two = datetime(2020, 11, 22)
        day_thee = datetime(2020, 12, 31)

        # An invalid query should just return None
        invalid_query_1 = ClassificationResultQuery(day_two, '3', True)
        invalid_query_2 = ClassificationResultQuery(day_one, 6, False)

        assert invalid_query_1.generate_query_string() == None
        assert invalid_query_2.generate_query_string() == None

        no_constraint_query = ClassificationResultQuery(None, None, None)
        assert no_constraint_query.generate_query_string() == 'SELECT * FROM classifications;'

        # Tests to ensure that each clause is properly formed
        query_day_1 = ClassificationResultQuery(day_one, None, None)
        query_day_2 = ClassificationResultQuery(day_two, None, None)
        query_day_3 = ClassificationResultQuery(day_thee, None, None)

        assert query_day_1.generate_query_string() == 'SELECT * FROM classifications WHERE 1600664400 <= timestamp AND timestamp < 1600750800;'
        assert query_day_2.generate_query_string() == 'SELECT * FROM classifications WHERE 1606024800 <= timestamp AND timestamp < 1606111200;'
        assert query_day_3.generate_query_string() == 'SELECT * FROM classifications WHERE 1609394400 <= timestamp AND timestamp < 1609480800;'

        query_class_0 = ClassificationResultQuery(None, 0, None)
        query_class_1 = ClassificationResultQuery(None, 1, None)
        query_class_2 = ClassificationResultQuery(None, 2, None)
        query_class_3 = ClassificationResultQuery(None, 3, None)
        query_class_4 = ClassificationResultQuery(None, 4, None)
        query_class_5 = ClassificationResultQuery(None, 5, None)

        assert query_class_0.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 0;'
        assert query_class_1.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 1;'
        assert query_class_2.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 2;'
        assert query_class_3.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 3;'
        assert query_class_4.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 4;'
        assert query_class_5.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 5;'

        query_signature_true = ClassificationResultQuery(None, None, True)
        query_signature_false = ClassificationResultQuery(None, None, False)

        assert query_signature_true.generate_query_string() == 'SELECT * FROM classifications WHERE has_signature = 1;'
        assert query_signature_false.generate_query_string() == 'SELECT * FROM classifications WHERE has_signature = 0;'

        # Tests to ensure that clauses can be combined properly
        query_combo_1 = ClassificationResultQuery(day_one, 0, None)
        query_combo_2 = ClassificationResultQuery(day_one, None, False)
        query_combo_3 = ClassificationResultQuery(None, 4, True)
        query_combo_all = ClassificationResultQuery(day_one, 5, False)

        assert query_combo_1.generate_query_string() == 'SELECT * FROM classifications WHERE 1600664400 <= timestamp AND timestamp < 1600750800 AND classification = 0;'
        assert query_combo_2.generate_query_string() == 'SELECT * FROM classifications WHERE 1600664400 <= timestamp AND timestamp < 1600750800 AND has_signature = 0;'
        assert query_combo_3.generate_query_string() == 'SELECT * FROM classifications WHERE classification = 4 AND has_signature = 1;'
        assert query_combo_all.generate_query_string() == 'SELECT * FROM classifications WHERE 1600664400 <= timestamp AND timestamp < 1600750800 AND classification = 5 AND has_signature = 0;'
        

    # Test inserting the record
    def test_insert_record_command(self):
        invalid_table_row  = ClassificationResultTableRow('1610121696.file.png', -1000, True)
        assert insert_record_command(invalid_table_row) == -1

        valid_table_row = ClassificationResultTableRow('1610121696.this.is.a.valid.filename.pdf', 1, False)
        assert insert_record_command(valid_table_row) == 0

        # Ensure that the record is being inserted with a SQL query
        conn = sqlite3.connect(identidoc_db)

        c = conn.cursor()
        c.execute('SELECT * FROM classifications;')
        
        results = c.fetchall()

        conn.close()

        assert len(results) == 1
        assert results[0] == (1610121696, 'this.is.a.valid.filename.pdf', 1, 0)

    
    # This object should only be accessed from within the database file, and should only hold
    # data that comes from the database, which has already been validated when it was put into the
    # database. No built in validation, and it can be assumed that it is always valid
    def test_QueryResultRow(self):
        result_row_1 = QueryResultRow((1610121696, 'this.is.a.valid.filename.pdf', 1, 0))
        result_row_2 = QueryResultRow((1610124814, 'file.png', 2, 1))
        
        assert result_row_1.timestamp == 1610121696
        assert result_row_1.filename == 'this.is.a.valid.filename.pdf'
        assert result_row_1.classification == 1
        assert result_row_1.has_signature == 0

        assert result_row_2.timestamp == 1610124814
        assert result_row_2.filename == 'file.png'
        assert result_row_2.classification == 2
        assert result_row_2.has_signature == 1
    
    
    # Ensure that the toJSON function produces a valid JSON
    def test_QueryResultRow_toJSON(self):
        result_row_1 = QueryResultRow((1610121696, 'this.is.a.valid.filename.pdf', 1, 0))
        result_row_2 = QueryResultRow((1610124814, 'file.png', 2, 1))

        is_valid_JSON_1 = self.is_json(result_row_1.toJSON())
        is_valid_JSON_2 = self.is_json(result_row_2.toJSON())

        assert is_valid_JSON_1
        assert is_valid_JSON_2


    # Testing a basic query - have to insert records into the database to start
    def test_retrieve_records_query_single_record(self):
        # Insert a record into the database and ensure the transaction is successful
        # if this assert statement fails, we have much larger issues than this unit test
        valid_table_row = ClassificationResultTableRow('1610121696.this.is.a.valid.filename.pdf', 1, False)
        assert insert_record_command(valid_table_row) == 0

        # Execute the basic query and validate it returns the one record inserted in the database
        query_result_1 = retrieve_records_query(None, None, None)

        assert len(query_result_1) == 1
        assert query_result_1[0].classification == 1
        assert query_result_1[0].filename == 'this.is.a.valid.filename.pdf'
        assert query_result_1[0].has_signature == 0
        assert query_result_1[0].timestamp == 1610121696

        date_file_was_uploaded = datetime(2021, 1, 8)
        date_file_was_not_uploaded = datetime(2000, 1, 1)

        # Query based on date
        query_result_2 = retrieve_records_query(date_file_was_uploaded, None, None)
        query_result_3 = retrieve_records_query(date_file_was_not_uploaded, None, None)

        assert len(query_result_2) == 1
        assert len(query_result_3) == 0

        # Query based on classification
        query_result_4 = retrieve_records_query(None, 1, None)
        query_result_5 = retrieve_records_query(None, 0, None)

        assert len(query_result_4) == 1
        assert len(query_result_5) == 0

        # Query based on signature
        query_result_6 = retrieve_records_query(None, None, False)
        query_result_7 = retrieve_records_query(None, None, True)

        assert len(query_result_6) == 1
        assert len(query_result_7) == 0


        # Query with multiple clauses

        # These query results should return the value
        query_result_8 = retrieve_records_query(date_file_was_uploaded, 1, None)
        query_result_9 = retrieve_records_query(date_file_was_uploaded, None, False)
        query_result_10 = retrieve_records_query(None, 1, False)
        query_result_11 = retrieve_records_query(date_file_was_uploaded, 1, False)

        assert len(query_result_8) == 1
        assert len(query_result_9) == 1
        assert len(query_result_10) == 1
        assert len(query_result_11) == 1

        # These query results should not return the value
        query_result_12 = retrieve_records_query(date_file_was_uploaded, 0, None)
        query_result_13 = retrieve_records_query(date_file_was_uploaded, 1, True)
        query_result_14 = retrieve_records_query(date_file_was_uploaded, None, True)
        query_result_15 = retrieve_records_query(None, 1, True)

        assert len(query_result_12) == 0
        assert len(query_result_13) == 0
        assert len(query_result_14) == 0
        assert len(query_result_15) == 0
    

    def test_retrieve_records_query_multiple_records(self):
        self.create_database_configuration_one()

        date = datetime(2020, 9, 21)

        query_result_1 = retrieve_records_query(date, None, None)
        assert len(query_result_1) == 240

        for classification_num in range(6):
            for has_signature in [True, False]:
                query_no_date = retrieve_records_query(None, classification_num, has_signature)
                query_date = retrieve_records_query(date, classification_num, has_signature)

                assert len(query_no_date) == 20
                assert len(query_date) == 20
    

    # Ensure the timezone conversion works correctly
    def test_retrieve_records_query_tricky_timestamps_1(self):
        assert insert_record_command(ClassificationResultTableRow('1600664399.test.pdf', 5, True)) == 0 # 9/20/2020 11:59:59 PM CST
        assert insert_record_command(ClassificationResultTableRow('1600664400.test.pdf', 5, True)) == 0 # 9/21/2020 12:00:00 AM CST

        date = datetime(2020, 9, 21)

        query_result = retrieve_records_query(date, None, None)

        assert len(query_result) == 1

    
    def test_retrieve_records_query_tricky_timestamps_2(self):
        assert insert_record_command(ClassificationResultTableRow('1600750799.test.pdf', 5, True)) == 0 # 9/21/2020 11:59:59 PM CST
        assert insert_record_command(ClassificationResultTableRow('1600750800.test.pdf', 5, True)) == 0 # 9/22/2020 12:00:00 AM CST

        date = datetime(2020, 9, 21)

        query_result = retrieve_records_query(date, None, None)

        assert len(query_result) == 1



    # Called at the conclusion of every unit test.
    # Removes all records from the table but leaves the table
    def tearDown(self):
        sql_delete_records = """DELETE FROM classifications;"""

        conn = sqlite3.connect(identidoc_db)

        c = conn.cursor()
        c.execute(sql_delete_records)
        conn.commit()
        conn.close()

    
    ####################
    #                  #
    # HELPER FUNCTIONS #
    #                  #
    ####################

    # This is a simple database configuration with 240 records
    #
    # All records were "uploaded/created" on 9/21/2020
    # 120 records have signatures (20 of each classification 0-6)
    # 120 records don't have signatures (20 of each classification 0-6)
    def create_database_configuration_one(self):
        for record_num in range(120):
            insert_record_command(ClassificationResultTableRow(str(1600680600 + record_num) + '.signature.pdf', record_num % 6, True))

        for record_num in range(120):
            insert_record_command(ClassificationResultTableRow(str(1600684200 + record_num) + '.no_signature.pdf', record_num % 6, False))


    @staticmethod
    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True