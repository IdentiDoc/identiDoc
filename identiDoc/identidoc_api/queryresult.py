# RESTful API Resource for query

from flask_restful import Resource

class QueryResult(Resource):
    def get(self, date):
        return { "result" : "These are the classification results from " + date }