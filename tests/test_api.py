import unittest
import requests

from identidoc import construct_application

# Unit Tests for the API
class TestAPI(unittest.TestCase):
    BASE = "http://127.0.0.1:5000/"

    def setUp(self):
        construct_application()
        pass


    def tearDown(self):
        pass


    # Testing the query call
    def test_query(self):
        query_response_1 = requests.get(self.BASE + "query/9-21-1998")
        query_response_2 = requests.get(self.BASE + "query/10-13-2020")
        query_response_3 = requests.get(self.BASE + "query/1-1-1970")

        result1 = query_response_1.status_code
        result3 = query_response_3.status_code
        result2 = query_response_2.status_code

        self.assertEqual(result1, 200)
        self.assertEqual(result2, 200)
        self.assertEqual(result3, 200)


    # Testing File Upload
    def test_file_upload(self):
        file1 = {
            'FILE_NAME': ('file1.txt', open('./files_to_upload/file1.txt', 'rb')),
        }

        file2 = {
            'FILE_NAME': ('file2.txt', open('./files_to_upload/file2.txt', 'rb')),
        }


        file3 = {
            'FILE_NAME': ('file3.txt', open('./files_to_upload/file3.txt', 'rb')),
        }


        upload_response_1 = requests.post(self.BASE + "upload", files=file1)
        upload_response_2 = requests.post(self.BASE + "upload", files=file2)
        upload_response_3 = requests.post(self.BASE + "upload", files=file3)

        result1 = upload_response_1.status_code
        result2 = upload_response_2.status_code
        result3 = upload_response_3.status_code

        self.assertEqual(result1, 200)
        self.assertEqual(result2, 200)
        self.assertEqual(result3, 200)

if __name__ == '__main__':
    unittest.main()
