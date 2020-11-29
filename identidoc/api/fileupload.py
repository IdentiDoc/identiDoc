# RESTful API Resource for file uploads

import os
from flask_restful import Resource, request
from werkzeug.utils import secure_filename

# List of allowed file extensions
file_extensions=['PDF','PNG','JPG','JPEG','TXT']

UPLOAD_PATH = os.environ.get('UPLOAD_PATH','./identidoc_uploads')

if not os.path.exists(UPLOAD_PATH):
    os.makedirs(UPLOAD_PATH)

class FileUpload(Resource):
    def post(self):
        file = request.files['FILE_NAME']
        # TODO: Append a timestamp as a unique identifier to the filename
        filename = secure_filename(file.filename)

        if '.' in filename and filename.rsplit('.', 1)[1].upper() in file_extensions:
            file.save(os.path.join(UPLOAD_PATH, filename))
            return{ "Saved as" : filename }
        else:
            return{ "Unsupported File Format" : filename }
