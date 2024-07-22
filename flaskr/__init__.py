#Create an __init__ file that will serve as an application factory

"""
Instead of creating a Flask instance globally, you will create it inside a function. This function is known as
the application factory. Any configuration, registration, and other setup the application needs will happen inside
the function, then the application will be returned.
"""

import os
from flask import Flask
from . import auth
from . import db

#Main code of the application factory.
def create_app(test_config=None):
    #Create the app and cofigure it
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="random_pass",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    #Configuration settings
    if test_config is None:
        #Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        #Load the test config if passed in
        app.config.from_mapping(test_config)

    #Use a try catch method to ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    #Test page
    @app.route("/")
    def hello_method():
        str = "Hello, mf!"

        return (str)

    #Registers the blueprint to the application factory
    app.register_blueprint(auth.bp)
    #Call the function from the db class
    db.init_app(app)

    return app