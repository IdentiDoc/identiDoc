All backend code has been moved to this directory and converted into modules

app.py is the main file that contains the factory method to create the application. This file can be run directly

identidoc_api/ - This directory holds all of the api stuff. This is importable as a python module

services/ - This directory holds all of the services (all subtasks of classificaiton will go here). This is importable as a python module

uploads/ - This is the upload directory (for now at least) - It gets created as the application is run