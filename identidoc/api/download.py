import os

from flask import send_file
from flask_restful import Resource


PATH_TO_FILE = os.environ['IDENTIDOC_UPLOAD_PATH']


class Download(Resource):
    def get(self, filename):
        filepath = os.path.join(PATH_TO_FILE, filename)

        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)

        return '', 204
