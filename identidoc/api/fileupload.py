# RESTful API Resource for file uploads

import os
from datetime import datetime
from flask_restful import Resource, request
from werkzeug.utils import secure_filename

# List of allowed file extensions
file_extensions=['PDF','PNG','JPG','JPEG','TXT','HEIC']

UPLOAD_PATH = os.environ.get('UPLOAD_PATH','./identidoc_uploads')

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

class FileUpload(Resource):
    def post(self):
        file = request.files['file']

        filename = secure_filename(file.filename)

        if self.valid_filename(filename):
            filename = self.add_timestamp(filename)
            file.save(os.path.join(UPLOAD_PATH, filename))
            
            return { 'message' : 'File successfully uploaded.' }
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


