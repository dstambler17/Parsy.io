import pytest
from flaskApp import create_app
from flaskApp import db as _db
from flaskApp import bcrypt as _bcrypt

@pytest.fixture(scope='session')
def app():
    _app = create_app(offline=False)
    _app.debug = True
    return _app

@pytest.fixture(scope='session')
def bcrypt(app):
    _bcrypt.app = app
    return _bcrypt

@pytest.fixture(scope='session')
def db(app):
    _db.app = app
    return _db


@pytest.fixture(scope='session')
def test_app(app):
    return app.test_client()
