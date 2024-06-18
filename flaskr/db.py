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

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as file:
        db.executescript(file.read().decode("utf8"))

@click.command("init_db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Database is initialized")

def close_db(e=None):
    db=g.pop("db", None)

    if db is not None:
        db.close()