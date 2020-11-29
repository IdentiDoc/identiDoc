# Application file for the identiDoc Flask application
# This file includes the factory function to create an instance of the identiDoc system

from flask import Flask, render_template

import identidoc.api as identidoc_api

app = Flask(__name__)

# Set the application configurations
# 24 MB
#
# Current issue: Not doing anything. TODO - ensure they're doing something.
# app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024
# app.config['UPLOAD_FOLDER'] = './uploads'

# Construct the RESTful API - Check identidoc_api module for this function (in __init__.py)
identidoc_api.construct_api(app)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)     # This value will be false in production
