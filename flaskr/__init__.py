#Create an __init__ file that will serve as an application factory

"""
Instead of creating a Flask instance globally, you will create it inside a function. This function is known as
the application factory. Any configuration, registration, and other setup the application needs will happen inside
the function, then the application will be returned.
"""

import os
from flask import Flask