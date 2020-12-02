# RESTful API Resource for file uploads

import os
from datetime import datetime
from flask import send_file
from flask_restful import Resource, request
from werkzeug.utils import secure_filename

import identidoc.services

# List of allowed file extensions
file_extensions=['PDF','PNG','JPG','JPEG','TXT','HEIC']

UPLOAD_PATH = os.environ.get('UPLOAD_PATH','./identidoc_uploads')

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
            
            return send_file(extracted_text_filepath, attachment_filename=orig_filename + '.txt', as_attachment=True)
        else:
            return { 'message' : 'Unsupported file format.' }, 400

    @staticmethod
    def valid_filename(filename):
        if '.' in filename:
            if filename.rsplit('.', 1)[1].upper() in file_extensions:
                return True

        return False

    @staticmethod
    def add_timestamp(filename):
        now = datetime.now()
        timestamp = now.strftime('%d%m%Y%H%M%S%f')
        return timestamp + '.' + filename


