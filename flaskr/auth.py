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

        # The user data is queried first and then stored into a variable
        # The fetchone() returns a specified row from the query
        user = db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = "Incorrect username"

        # check_password_hash() hashes the submitted password in the same method it is hashed and then compares the two.
        elif not check_password_hash(user[password], password):
            error = "Incorrect password"

        if error is None:
            #Session is dict that stores data across requests, When validation is done the id of the user is stored in a new session
            """The data is stored in a cookie that is sent to the browser,
             and the browser then sends it back with subsequent requests. 
             Flask securely signs the data so that it can’t be tampered with."""
            session.clear()
            session["user_id"] = user["id"]

            return redirect(url_for("index"))

        flash(error)
    return  render_template("auth/login.html")

#Function that runs before the view function, regardless of what URL is requested.
@bp.before_app_request
#Function that checks if user_id is stored in the session and gets the data from it.
def load_loggin_user():
    user_id = session.get("user_id")

    if user_id is None:
        #If user_id is null on the session, then g.user will be none
        g.user = None
    else:
        #The data from the session is stored on g.user, which lasta for the length of the request
        g.user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()

#Function for user logout
#To logout we need to remove the user id from the session. Then the "load_logged_in_user" will not load a user on subsequent requests
@bp.route("/logout")
def logout():
    #Clears the data inside the session variable
    session.clear()
    #Returns to the initial view
    return redirect(url_for("index"))

#Require logins for views that require a "user"
#This decorator returns a new view function that is wrapped on the original view it is applied to.
#The function checks if a user is loaded and logged in and works normally, users who have not logged in gets redirected if otherwise.
def login_required(view):
    @functools.wraps(view)

    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))



        return view(**kwargs)

    return wrapped_view()