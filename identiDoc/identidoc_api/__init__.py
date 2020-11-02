from .fileupload import *
from .queryresult import *

from flask_restful import Api

def construct_api(app):
    api = Api(app)

    api.add_resource(QueryResult, "/query/<string:date>")
    api.add_resource(FileUpload, "/upload")

    return api