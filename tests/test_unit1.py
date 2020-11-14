# importing the required modules

import unittest
import test_req

#class for unit test
class test_unit1(unittest.TestCase):


	#first test to see if the  http query response is working correctly or not
	def test_query(self):
		result1 = test_req.query_response_1.status_code
		self.assertEqual(result1,200)
		result2 = test_req.query_response_2.status_code
		self.assertEqual(result2,200)
		result3 = test_req.query_response_3.status_code
		self.assertEqual(result3,200)

	#second test to see if the http upload response is working correctly or not
	def test_response(self):
		result1 = test_req.upload_response_1.status_code
		self.assertEqual(result1,200)
		result2 = test_req.upload_response_2.status_code
		self.assertEqual(result2,200)
		result3 = test_req.upload_response_3.status_code
		self.assertEqual(result3,200)

	


if __name__ == '__main__':

    unittest.main()