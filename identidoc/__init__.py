# Application file for the identiDoc Flask application
# This file includes the factory function to create an instance of the identiDoc system

from flask import Flask, render_template

import identidoc.api as identidoc_api
import identidoc.services

app = Flask(__name__)

# Set the file upload size to 25 MB
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024

# Construct the RESTful API - Check identidoc_api module for this function (in __init__.py)
identidoc_api.construct_api(app)

# Ensure that the application can connect to the database
identidoc.services.validate_database()


@app.route('/')
def load_index_page():
    return render_template('index.html')


@app.route('/nav')
def load_nav():
    return render_template('nav.html')


@app.route('/upload')
def load_upload_file_page():
    return render_template('upload.html')


@app.route('/query')
def load_query_page():
    return render_template('query.html')


# Runs identiDoc locally
if __name__ == '__main__':
    app.run(debug=True)
