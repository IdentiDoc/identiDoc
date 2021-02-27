from flask_restful import Api

from .fileupload import *
from .queryresult import *

def construct_api(app):
    api = Api(app)

    api.add_resource(QueryResult, "/api/query/<string:UI_date>/<string:UI_classification>/<string:UI_signature>")
    api.add_resource(FileUpload, "/api/upload")

    return api