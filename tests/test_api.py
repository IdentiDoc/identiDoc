import unittest
import warnings

from identidoc import app


# Decorator to ignore ResourceWarnings when "uploading" files
def ignore_resource_warnings(test_func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)
    return do_test

# Unit Tests for the API
class TestAPI(unittest.TestCase):

    # This is the setup funciton for the unit tests
    def setUp(self):
        self.app = app
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


    @ignore_resource_warnings
    def test_file_upload_functional(self):
        # Just testing the upload of 3 test files
        resp1 = self.post_file('./tests/files_to_upload/file1.txt')
        resp2 = self.post_file('./tests/files_to_upload/file2.txt')
        resp3 = self.post_file('./tests/files_to_upload/file3.txt')

        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)

    
    @ignore_resource_warnings
    def test_file_upload_all_valid_file_types(self):
        #resp_heic = self.post_file('./tests/files_to_upload/example.heic')
        resp_jpeg = self.post_file('./tests/files_to_upload/example.jpeg')
        resp_jpg = self.post_file('./tests/files_to_upload/example.jpg')
        resp_pdf = self.post_file('./tests/files_to_upload/example.pdf')
        resp_png = self.post_file('./tests/files_to_upload/example.png')

        #self.assertEqual(resp_heic.status_code, 200)
        self.assertEqual(resp_jpeg.status_code, 200)
        self.assertEqual(resp_jpg.status_code, 200)
        self.assertEqual(resp_pdf.status_code, 200)
        self.assertEqual(resp_png.status_code, 200)


    @ignore_resource_warnings
    def test_file_upload_invalid_file_types(self):
        resp_invalid1 = self.post_file('./tests/files_to_upload/invalid.bmp')
        resp_invalid2 = self.post_file('./tests/files_to_upload/invalid.mp4')
        resp_invalid3 = self.post_file('./tests/files_to_upload/invalid.ABC')

        self.assertEqual(resp_invalid1.status_code, 400)
        self.assertEqual(resp_invalid2.status_code, 400)
        self.assertEqual(resp_invalid3.status_code, 400)

        # Ensure correct message
        self.assertEqual(resp_invalid1.json['message'], 'Unsupported file format.')
        self.assertEqual(resp_invalid2.json['message'], 'Unsupported file format.')
        self.assertEqual(resp_invalid3.json['message'], 'Unsupported file format.')

    @ignore_resource_warnings
    def test_file_upload_file_too_large(self):
        resp_large1 = self.post_file('./tests/files_to_upload/large.pdf')
        resp_large2 = self.post_file('./tests/files_to_upload/large.png')

        self.assertEqual(resp_large1.status_code, 413)
        self.assertEqual(resp_large2.status_code, 413)




    # Helper function to post file uploads in the correct format
    def post_file(self, filepath):
        return self.test_client.post(
            '/upload',
            data = {
                'file' : ( open(filepath, 'rb'), filepath ),
            }
        )


if __name__ == '__main__':
    unittest.main()
