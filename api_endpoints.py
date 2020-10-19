# This file includes all of the endpoints for the API that will be available to the client
#
# Author - Jonathan Marek
# Date  - 10/13/2020
import os
from flask import Flask
from flask_restful import Api, Resource, request

from fake_backend import *

app = Flask(__name__)
api = Api(app)


# Resource that will return the result of a query for classification results
class QueryResult(Resource):
    def get(self, date):

        ClassificationQuery = ClassificationResultQuery(date)
        result = GetClassificationQueryResults(ClassificationQuery)
        return {"result": result}

#Resource that will upload the given file to the server(local system in this case)        
class FileUpload(Resource):
    def post(self):
        file=request.files['FILE_NAME']
        filename=file.filename
        file.save(os.path.join(".",filename))
        return{"Saved as":filename}


api.add_resource(QueryResult, "/Query/<string:date>")
api.add_resource(FileUpload,"/upload")

if __name__ == "__main__":
    app.run(debug=True)     # This value will be false in production