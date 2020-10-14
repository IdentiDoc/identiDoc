# This file includes all of the endpoints for the API that will be available to the client
#
# Author - Jonathan Marek
# Date  - 10/13/2020

from flask import Flask
from flask_restful import Api, Resource

from fake_backend import *

app = Flask(__name__)
api = Api(app)


# Resource that will return the result of a query for classification results
class QueryResult(Resource):
    def get(self, date):

        ClassificationQuery = ClassificationResultQuery(date)
        result = GetClassificationQueryResults(ClassificationQuery)

        return {"result": result}
        

api.add_resource(QueryResult, "/Query/<string:date>")

if __name__ == "__main__":
    app.run(debug=True)     # This value will be false in production