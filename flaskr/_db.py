"""Functions which handle interactions with the database."""

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import check_password_hash, generate_password_hash


### CONNECTIONS ###


def get_db():
    """Open database connection and return the database object.

    Returns:
        sqlite3.Connection: the connection object.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def _close_db(e=None):
    """Close the database connection."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Initialise the database."""
    db = get_db()
    with current_app.open_resource("sql/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")  # allows function calling from CLI
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Initialise the app.

    Args:
        app (flask.Flask): The Flask application to setup.
    """
    app.teardown_appcontext(_close_db)
    app.cli.add_command(init_db_command)


### USER INTERACTIONS ###


def get_user_id(username):
    """Get the user id based on username.

     Args:
        username (str): The username to get the id for.

    Returns:
        sqlite3.Row: The row containing the ID.

    """
    db = get_db()
    return db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()


def get_user(username):
    """Get all info for a user based on username.

    Args:
        username (str): The username to get the information about.

    Returns:
        sqlite3.Row: The row containing the information.

    """
    db = get_db()
    return db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()


def add_user(username, password):
    """Add the specified user with password to the database.

    The password will be hashed using werkzeug.security function.

    Args:
        username (str): The username to add.
        password (str): The password to add.
    """
    db = get_db()
    db.execute(
        "INSERT INTO user (username, password) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    db.commit()


def get_user_by_id(user_id):
    """Return the user entry based on the user id.

    Args:
        user_id (str): The user id to get the information about.

    Returns:
        sqlite3.Row: The row containing the information.

    """
    db = get_db()
    return db.execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()


### BLOG INTERACTIONS ###


def get_post(post_id):
    """Return the blog post by id."""
    db = get_db()
    return db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (post_id,),
    ).fetchone()


def get_posts():
    """Return all blog posts.

    Returns:
        list(sqlite3.Row): A list of blog post entries.
    """
    db = get_db()
    return db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()


def create_post(user_id, title, body):
    """Create a post entry for the given user.

    Args:
        user_id (str): The user id of author.
        title (str): The title of the blog post.
        body (str): The main body of text for the post.
    """
    db = get_db()
    db.execute(
        "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
        (title, body, user_id),
    )
    db.commit()


def update_post(post_id, title, body):
    """Update the post with a new title and body.

    Args:
        post_id (str): the id of the post to update.
        title (str): the new title of the post.
        body (str): the new body of the post.
    """
    db = get_db()
    db.execute(
        "UPDATE post SET title = ?, body = ?" " WHERE id = ?", (title, body, post_id)
    )
    db.commit()


def delete_post(post_id):
    """Delete the post.

    Args:
        post_id (str): the id of the post to delete.
    """
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (post_id,))
    db.commit()
