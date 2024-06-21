"""The appication will use a SQLite database to store the users and their
respective posts, it comes built in with python as a module"""

import sqlite3
import click

from flask import current_app, g

def get_db():
    #g is a special object that holds data related to the connection that can be used by multiple functions
    if "db" not in g:
        #Establish a connection to the file pointed by the "DATABASE" key from the configs.
        g.db = sqlite3.connect(
            #Current app is another special object that points to the request, it will be called when the application factory
            #has created the application itself.
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row

    return g.db

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))

@click.command("init_db")
def init_db_command():
    #Clear existing data if there is any and Initializes the database
    init_db()
    click.echo("Database is initialized")

def close_db(e=None):
    db=g.pop("db", None)

    if db is not None:
        db.close()