from flask_restful import Api

from .fileupload import *
from .queryresult import *

def construct_api(app):
    api = Api(app)

    api.add_resource(QueryResult, "/api/query/<string:date>")
    api.add_resource(FileUpload, "/api/upload")

    return api