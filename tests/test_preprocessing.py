import unittest
from identidoc.services import preprocessing

class TestPreprocessing(unittest.TestCase):

    file_path = 'test_forms/'
    # converted image files
    aa = preprocessing.file_conversion(file_path + 'aa.png')
    coa = preprocessing.file_conversion(file_path + 'coa.png')
    si = preprocessing.file_conversion(file_path + 'si.png')
    voh = preprocessing.file_conversion(file_path + 'voh.png')
    voi = preprocessing.file_conversion(file_path + 'voi.png')    

    def test_preprocess_file(self):

        aa = preprocessing.preprocess_file(self.file_path + 'aa.png')
        coa = preprocessing.preprocess_file(self.file_path + 'coa.png')
        si = preprocessing.preprocess_file(self.file_path + 'si.png')
        voh = preprocessing.preprocess_file(self.file_path + 'voh.png')
        voi = preprocessing.preprocess_file(self.file_path + 'voi.png')
        
        self.assertIn('academic advisor', aa.lower())
        self.assertIn('cost of attendance', coa.lower())
        self.assertIn('student information', si.lower())
        self.assertIn('household information', voh.lower())
        self.assertIn('verification of income', voi.lower())

    def test_rotate_image(self):
        
        self.assertIsNotNone(preprocessing.rotate_image(self.aa))
        self.assertIsNotNone(preprocessing.rotate_image(self.coa))
        self.assertIsNotNone(preprocessing.rotate_image(self.si))
        self.assertIsNotNone(preprocessing.rotate_image(self.voh))
        self.assertIsNotNone(preprocessing.rotate_image(self.voi))

    def test_image_pre_processing(self):

        aa = preprocessing.image_pre_processing(preprocessing.rotate_image(self.aa))
        coa = preprocessing.image_pre_processing(preprocessing.rotate_image(self.coa))
        si = preprocessing.image_pre_processing(preprocessing.rotate_image(self.si))
        voh = preprocessing.image_pre_processing(preprocessing.rotate_image(self.voh))
        voi = preprocessing.image_pre_processing(preprocessing.rotate_image(self.voi))

        self.assertIsNotNone(aa)
        self.assertIsNotNone(coa)
        self.assertIsNotNone(si)
        self.assertIsNotNone(voh)
        self.assertIsNotNone(voi)


    def test_tesseract_text_extraction(self):
        
        aa = preprocessing.tesseract_text_extraction(preprocessing.image_pre_processing(preprocessing.rotate_image(self.aa)))
        coa = preprocessing.tesseract_text_extraction(preprocessing.image_pre_processing(preprocessing.rotate_image(self.coa)))
        si = preprocessing.tesseract_text_extraction(preprocessing.image_pre_processing(preprocessing.rotate_image(self.si)))
        voh = preprocessing.tesseract_text_extraction(preprocessing.image_pre_processing(preprocessing.rotate_image(self.voh)))
        voi = preprocessing.tesseract_text_extraction(preprocessing.image_pre_processing(preprocessing.rotate_image(self.voi)))

        self.assertIn('academic advisor', aa.lower())
        self.assertIn('cost of attendance', coa.lower())
        self.assertIn('student information', si.lower())
        self.assertIn('household information', voh.lower())
        self.assertIn('verification of income', voi.lower())

    def test_file_conversion(self):

        self.assertIsNotNone(self.aa)
        self.assertIsNotNone(self.coa)
        self.assertIsNotNone(self.si)
        self.assertIsNotNone(self.voh)
        self.assertIsNotNone(self.voi)