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
        user = User(email="joe@example.com", password="password", first_name="Joe", last_name="Admin", is_admin=True)
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

    yield client

    with app.app_context():
        db.drop_all()

def test_login(client):
    response = client.post('/login', json={"email": "joe@example.com", "password": "password"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "access_token" in data

def test_admin_access(client):
    response = client.post('/login', json={"email": "joe@example.com", "password": "password"})
    access_token = json.loads(response.data)["access_token"]

    response = client.post('/admin/data', headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
