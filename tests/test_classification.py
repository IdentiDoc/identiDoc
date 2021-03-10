import unittest
from identidoc.services import classification
from identidoc.services import preprocessing

class TestClassification(unittest.TestCase):

    file_path = 'test_forms/'
    # extracted text
    aa = preprocessing.preprocess_file(file_path + 'aa.png')
    coa = preprocessing.preprocess_file(file_path + 'coa.png')
    si = preprocessing.preprocess_file(file_path + 'si.png')
    voh = preprocessing.preprocess_file(file_path + 'voh.png')
    voi = preprocessing.preprocess_file(file_path + 'voi.png')  

    def test_predict_document_class(self):

        self.assertEqual(classification.predict_document_class(self.coa), 1)
        self.assertEqual(classification.predict_document_class(self.voh), 2)
        self.assertEqual(classification.predict_document_class(self.voi), 3)
        self.assertEqual(classification.predict_document_class(self.aa), 4)
        self.assertEqual(classification.predict_document_class(self.si), 5)

    def test_vectorizer(self):
        
        self.assertIsNotNone(classification.vectorizer(self.aa))
        self.assertIsNotNone(classification.vectorizer(self.coa))
        self.assertIsNotNone(classification.vectorizer(self.si))
        self.assertIsNotNone(classification.vectorizer(self.voh))
        self.assertIsNotNone(classification.vectorizer(self.voi))

    def test_classifier(self):

        aa = (classification.vectorizer(self.aa))
        coa = (classification.vectorizer(self.coa))
        si = (classification.vectorizer(self.si))
        voh = (classification.vectorizer(self.voh))
        voi = (classification.vectorizer(self.voi))
        
        self.assertEqual(classification.classifier(coa), 1)
        self.assertEqual(classification.classifier(voh), 2)
        self.assertEqual(classification.classifier(voi), 3)
        self.assertEqual(classification.classifier(aa), 4)
        self.assertEqual(classification.classifier(si), 5)