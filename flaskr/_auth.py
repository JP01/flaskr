"""Functions defining the authorisation pages."""

import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash

from ._db import add_user, get_user, get_user_id, get_user_by_id

_BP = Blueprint("auth", __name__, url_prefix="/auth")
"""Global Blueprint object that will be used for auth page blueprints."""


def get_blueprint():
    """Get the auth page blueprint.

    Returns:
        flask.Blueprint: The auth page blueprint object.

    """
    return _BP


@_BP.route("/register", methods=("GET", "POST"))
def register():
    """Return the 'User Register' Page.

    Returns:
        str: the rendered register page html.

    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = ""

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif get_user_id(username) is not None:
            error = "User {} is already registered.".format(username)
        # no errors so we can safely add new user
        if not error:
            add_user(username, password)
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


def login_required(view):
    """Wrapper to determine if login is required and redirect to login page.

    Args:
        view (function): Wraps the view function so that access from non-logged
            in user will be redirected to the login page.

    Returns:
        function: The requested view function if user is logged in,
        otherwise login page view function.

    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


@_BP.route("/login", methods=("GET", "POST"))
def login():
    """Return the 'User Login' Page.

    Returns:
        str: the rendered login page html.

    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = ""
        user = get_user(username)

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if not error:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@_BP.before_app_request
def load_logged_in_user():
    """Load a logged in user to the session."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)


@_BP.route("/logout")
def logout():
    """Log user out by clearing the session.

    Returns:
        str: the rendered index page html.

    """
    session.clear()
    return redirect(url_for("index"))
