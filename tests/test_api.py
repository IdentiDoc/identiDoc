import unittest

from identidoc import construct_application

# Unit Tests for the API
class TestAPI(unittest.TestCase):

    # This is the setup funciton for the unit tests
    def setUp(self):
        self.app = construct_application(config='TEST')
        self.app.testing = True
        self.test_client = self.app.test_client()


    def tearDown(self):
        pass

    # Testing the query call returns a 200 response
    def test_query(self):
        query_response_1 = self.test_client.get('/query/5-23-2002')
        query_response_2 = self.test_client.get('/query/10-13-2020')
        query_response_3 = self.test_client.get('/query/1-1-1970')

        result1 = query_response_1.status_code
        result3 = query_response_3.status_code
        result2 = query_response_2.status_code

        self.assertEqual(result1, 200)
        self.assertEqual(result2, 200)
        self.assertEqual(result3, 200)
            
# TODO - Write a unit test for the file upload - Can think of several


if __name__ == '__main__':
    unittest.main()
