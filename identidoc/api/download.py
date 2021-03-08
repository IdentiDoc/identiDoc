import os

from flask import send_file
from flask_restful import Resource


PATH_TO_FILE = os.environ['IDENTIDOC_UPLOAD_PATH']


class Download(Resource):
    def get(self, filename):
        filepath = os.path.join(PATH_TO_FILE, filename)

        if os.path.exists(filepath):
            filename_without_timestamp = filename.split('.', 1)[1]
            return send_file(filepath, as_attachment=True, attachment_filename=filename_without_timestamp)

        return '', 204
