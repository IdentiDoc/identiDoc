# RESTful API Resource for query

from identidoc.services import classify_uploaded_file
from flask_restful import Resource

class QueryResult(Resource):
    def get(self, date, classification, signature):
        print(date)
        print(classification)
        print(signature)
        return { "result" : "These are the classification results from " + date }