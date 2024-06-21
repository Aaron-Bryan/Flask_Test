import functools

from flaskr.db import get_db

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


#Create a blueprint named auth
#__name__ is put on so that the blueprint itself knows where it is defined
#the url_prefix will be added to the URLs related with the blueprint
bp = Blueprint("auth", __name__, url_prefix="/auth")