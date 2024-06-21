#Create an __init__ file that will serve as an application factory

"""
Instead of creating a Flask instance globally, you will create it inside a function. This function is known as
the application factory. Any configuration, registration, and other setup the application needs will happen inside
the function, then the application will be returned.
"""

import os
from flask import Flask
from . import db


def create_app(test_config=None):
    #Create the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="random_pass",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass


    @app.route("/")
    def hello_method():
        str = "Hello, mf!"

        return (str)

    db.init_app(app)
    return app