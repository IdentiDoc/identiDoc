# RESTful API Resource for file uploads

import os
from flask_restful import Resource, request
from werkzeug.utils import secure_filename

from identidoc.services import get_current_time_as_POSIX_timestamp, classify_uploaded_file

# List of allowed file extensions
file_extensions=['PDF','PNG','JPG','JPEG','HEIC']

UPLOAD_PATH = os.environ['IDENTIDOC_UPLOAD_PATH']

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

class FileUpload(Resource):
    def post(self):
        file = request.files['file']

        orig_filename = secure_filename(file.filename)

        if self.valid_filename(orig_filename):
            filename = self.add_timestamp(orig_filename)
            saved_filepath = os.path.join(UPLOAD_PATH, filename)

            file.save(saved_filepath)
            
            document_classification = classify_uploaded_file(saved_filepath)
            
            return { 'classification' : str(document_classification) }, 200
        else:
            return { 'message' : 'Unsupported file format.' }, 400


    @staticmethod
    def valid_filename(filename):
        if '.' in filename:
            if filename.rsplit('.', 1)[1].upper() in file_extensions:
                return True

        return False


    @staticmethod
    # Updated - Replace this with a standard POSIX timestamp
    def add_timestamp(filename):
        timestamp = get_current_time_as_POSIX_timestamp()
        return str(timestamp) + '.' + filename


