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

#Setting the maximum file size allowed: 24MB in this case

app.config['MAX_CONTENT_LENGTH'] = 24*1024 * 1024

#List of allowed file extensions

file_extensions=['PDF','PNG','JPG','JPEG','TXT','DOC']

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
        if '.' in filename and filename.rsplit('.', 1)[1].upper() in file_extensions:
                file.save(os.path.join(".",filename))
                return{"Saved as":filename}
        else:
                return{"Unsupported File Format":filename}


api.add_resource(QueryResult, "/Query/<string:date>")
api.add_resource(FileUpload,"/upload")

if __name__ == "__main__":
    app.run(debug=True)     # This value will be false in production