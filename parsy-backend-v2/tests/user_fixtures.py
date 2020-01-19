import pytest
from flaskApp.models import User

@pytest.fixture
def delete_user(request, db):
    def _delete_user():
        user = User.query.filter_by(username='test_user').first()
        db.session.delete(user)
        db.session.commit()

    request.addfinalizer(_delete_user)
    return


@pytest.fixture
def create_user(request, db, bcrypt):
    password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='test_user', password=password, affiliation='student')
    db.session.add(user)
    db.session.commit()

    def _delete_user():
        user = User.query.filter_by(username='test_user').first()
        db.session.delete(user)
        db.session.commit()

    request.addfinalizer(_delete_user)
    return
