import unittest

from identidoc.api import FileUpload

class TestFileUploadHelpers(unittest.TestCase):
    def test_is_valid_filename(self):
        self.assertTrue(FileUpload.valid_filename('test.txt'))
        self.assertTrue(FileUpload.valid_filename('test.jpg'))
        self.assertTrue(FileUpload.valid_filename('test.jpeg'))
        self.assertTrue(FileUpload.valid_filename('test.pdf'))
        self.assertTrue(FileUpload.valid_filename('test.png'))

        self.assertTrue(FileUpload.valid_filename('1.2.3.4.5.6.7.8.png'))
        self.assertTrue(FileUpload.valid_filename('a_really.long.filename.with.lotsofperiods.txt'))

        self.assertFalse(FileUpload.valid_filename('file'))
        self.assertFalse(FileUpload.valid_filename('test.mp4'))

    
    def test_add_timestamp(self):
        filename = 'test.txt'
        self.assertTrue(FileUpload.add_timestamp(filename) != filename)

