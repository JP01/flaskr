"""Functions defining the blog pages."""

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from ._auth import login_required

from ._db import create_post, delete_post, get_post, get_posts, update_post

_BP = Blueprint("blog", __name__)
"""Global Blueprint object that will be used for blog page blueprints."""


def get_blueprint():
    """Get the blog page blueprint.

    Returns:
        flask.Blueprint: The blog page blueprint object.

    """
    return _BP


@_BP.route("/")
def index():
    """Return the 'Blog Index' page.

    Returns:
        str: The blogs index html.

    """
    posts = get_posts()
    return render_template("blog/index.html", posts=posts)


@_BP.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Return the 'Create Blog' page.

    Returns:
        str: The create blog post html.
    """
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            create_post(g.user["id"], title, body)
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def _get_post(post_id, check_author=True):
    """Get the post by ID or abort with an error.

    Args:
        post_id (str): the ID of the blog post to find.
        check_author (bool): Default=True. Wether to check if the current
            user is the author of the post.

    Returns:
        sqlite3.Row: The blog post database entry.

    """
    post = get_post(post_id)
    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@_BP.route("/<int:post_id>/update", methods=("GET", "POST"))
@login_required
def update(post_id):
    """Return the 'Update Post' page.

    Args:
        post_id (str): The id of the post to update.

    Returns:
        str: The update page html.

    """
    post = _get_post(post_id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            update_post(post_id, title, body)
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@_BP.route("/<int:post_id>/delete", methods=("POST",))
@login_required
def delete(post_id):
    """Delete post and return blog index.

    Args:
        post_id (str): The id of the post to delete.

    Returns:
        str: The index page html.

    """
    post = _get_post(post_id)
    delete_post(post["id"])
    return redirect(url_for("blog.index"))
