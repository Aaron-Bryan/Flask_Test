"""The appication will use a SQLite database to store the users and their
respective posts, it comes built in with python as a module"""

import sqlite3
import click

from flask import current_app, g

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory=sqlite3.Row

    return g.db

def init_db():
    database = get_db()

    with current_app.open_resource("schema.sql") as file:
        database.executescript(file.read().decode("utf8"))

def close_db(e=None):
    db=g.pop("db", None)

    if db is not None:
        db.close()