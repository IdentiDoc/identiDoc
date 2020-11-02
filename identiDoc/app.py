# Application file for the identiDoc Flask application
# This file includes the factory function to create an instance of the identiDoc system

from flask import Flask

import identidoc_api

# Factory method to construct the applicaiton.
# This should only change when being deployed
def construct_application(config=None):
    app = Flask(__name__)

    # Set the application configurations
    # 24 MB
    #
    # Current issue: Not doing anything. TODO - ensure they're doing something.
    # app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024
    # app.config['UPLOAD_FOLDER'] = './uploads'

    # Construct the RESTful API - Check identidoc_api module for this function (in __init__.py)
    api = identidoc_api.construct_api(app)

    return app, api


if __name__ == '__main__':
    app, api = construct_application()
    app.run(debug=True)     # This value will be false in production