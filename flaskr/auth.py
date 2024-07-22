import functools

from flaskr.db import get_db

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash


#Create a blueprint named auth and configure it with a prefix to add to the URLs it is related to.
bp = Blueprint("auth", __name__, url_prefix="/auth")

#Function for new user registration
#@bp.route Associates the URL "/register" with the register view function
@bp.route("/register", methods=("GET", "POST"))
def register():
    #"POST" the new user's data into the database
    if (request.method == "POST"):
        #"request.form" is a special dict that maps the respective inputs
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        error = None

        #If cases to check if the parameters are satisfied
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required"

        #If params are satisfied
        if error is None:
            #Insert the new user's data into the database
            try:
                #"db.execute" takes a sql query with the "?" as a placeholder
                #It's good practice to not directly input passwords into the database, hash them insteam with generate_password_hash
                db.execute("Insert Into user (username, password) Values (?, ?)",
                           (username, generate_password_hash(password)))
                #"db.commit" needs to be called to save the changes made
                db.commit()
            #An IntegrityError happens when the username already exists within the databse
            except db.IntegrityError:
                error = f"User {username} already exists"
            else:
                #After storing the new user's data into the database they are redirected to the login page
                #"redirect" generates a redirect response to the generated URL
                #"url_for" generates URL to the login view
                return redirect(url_for("auth.login"))

        #Ouputs the error message
        flash(error)

    return render_template("auth/register.html")

#Function for user login.
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

