# RESTful API Resource for file uploads

import os
from flask import send_file
from flask_restful import Resource, request
from werkzeug.utils import secure_filename

import identidoc.services

# List of allowed file extensions
file_extensions=['PDF','PNG','JPG','JPEG','TXT','HEIC']

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
            extracted_text_filepath = identidoc.services.preprocess_file(saved_filepath)
            
            #return send_file(extracted_text_filepath, attachment_filename=orig_filename + '.txt', as_attachment=True)
            return { 'message' : 'Upload Successful'}, 200
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
        timestamp = identidoc.services.get_current_time_as_POSIX_timestamp()
        return str(timestamp) + '.' + filename


