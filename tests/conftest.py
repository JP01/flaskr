"""Configure test fixtures and setup."""
import os
import tempfile

import pytest
from flaskr._factory import create_app
from flaskr._db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data/data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Yield a app for testing then clean up once done.

    Yields:
        flask.Flask: The test app.
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({"TESTING": True, "DATABASE": db_path, })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """Return a test client for the app.

    Args:
        app (flask.Flask): The application under test.

    Returns:
        flask.testing.FlaskClient: The test client.

    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Return a test cli runner for the app.

    Args:
        app (flask.Flask): The application under test.

    Returns:
        flask.testing.FlaskCliRunner: The test CLI runner.

    """
    return app.test_cli_runner()
