import pytest
from flask import json
from src import create_app
from src.models import db
from src.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

@pytest.fixture
def client():
    app = create_app("src.config.TestingConfig")
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        user = User(email="tester@example.com", password="password", first_name="Tester", last_name="User", is_admin=False)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.drop_all()

def test_login(client):
    response = client.post('/login', json={"email": "tester@example.com", "password": "password"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "access_token" in data
