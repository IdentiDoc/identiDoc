To setup:
    Make sure that you have python3 installed on your local machine.

    Install requirements with pip with the command "pip3 install -r requirements.txt"


To run:
    Use the command "python3 api_endpoints.py"

Endpoints:
    Return the database query results of all of the classification results that occur on the given date
    - A GET request with the URL "http://127.0.0.1:5000/query/<date>" where date is of the form mm-dd-yyyy
    - A POST request with the URL "http://127.0.0.1:5000/upload along with a form where the html should be of the form:
        
        <form method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value=Upload>
        </form>

There are example requests in the test_req.py file. You can run this file in another terminal
while the flask app is running to test requests. All requests should return code 200

NOTE: You'll have to change the filepaths in test_req.py to a file on your computer
