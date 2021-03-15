# This unit test ensures that the identidoc environment is correctly set up.
# If this unit test fails, the current version of identiDoc should not be deployed.

from identidoc.services.signaturedetection import signature_detection
import unittest
import os

class TestEnv(unittest.TestCase):
    # Add to this unit test as environment variables are created/modified
    def test_env_vars(self):
        upload_path = os.environ.get('IDENTIDOC_UPLOAD_PATH', 'ERROR')
        temp_path = os.environ.get('IDENTIDOC_TEMP_PATH', 'ERROR')
        db_path = os.environ.get('IDENTIDOC_DB', 'ERROR')
        classification_models = os.environ.get('IDENTIDOC_CLASSIFICATION_MODELS', 'ERROR')
        signature_detection - os.environ.get('IDENTIDOC_SIGNATURE_DETECTION', 'ERROR')

        assert upload_path != 'ERROR'
        assert temp_path != 'ERROR'
        assert db_path != 'ERROR'
        assert classification_models != 'ERROR'
        assert signature_detection != 'ERROR'
