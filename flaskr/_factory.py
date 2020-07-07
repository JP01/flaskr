"""Functions for create the flask app."""

import os

from flask import Flask

from . import _auth, _blog, _db


def create_app(test_config=None):
    """Create and configure the app.

    Args:
        test_config: additional configuration for the app.

    Returns:
        flask.Flask: the app object.

    """
    # create the flask object and use a local .instance directory
    app = Flask(
        __name__,
        instance_relative_config=True,
        instance_path=os.path.join(os.path.dirname(__file__), ".instance")
    )
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # setup the app
    _db.init_app(app)
    app.register_blueprint(_auth.get_blueprint())
    app.register_blueprint(_blog.get_blueprint())

    # anytime index or blog.index is called we associate it with '/' url
    app.add_url_rule("/", endpoint="index")

    return app
