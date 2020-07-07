"""Integration Tests for the :mod:`flaskr._factory` module."""


def test_create_app_main():
    """Test creating  app in normal mode."""
    from flaskr._factory import create_app

    assert not create_app().testing


def test_create_app_testing():
    """Test creating app in test mode."""
    from flaskr._factory import create_app

    assert create_app({"TESTING": True}).testing


def test_create_app_hello(client):
    """Test creating a basic helloworld app."""
    response = client.get("/hello")
    assert response.data == b"Hello, World!"
