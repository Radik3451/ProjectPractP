# test.py
import json
import pytest
from flask import Flask
from api import jobs_bp
from users import db, Jobs

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firm.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(jobs_bp)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_all_jobs(client):
    response = client.get('/api/jobs')
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, list)

def test_get_one_job(client):
    # Предположим, что у вас есть работа с id=1 в базе данных
    response = client.get('/api/jobs/1')
    assert response.status_code == 200
    data = json.loads(response.get_data(as_text=True))
    assert isinstance(data, dict)

def test_get_invalid_id_job(client):
    response = client.get('/api/jobs/invalid_id')
    assert response.status_code == 404

def test_get_nonexistent_job(client):
    response = client.get('/api/jobs/999')
    assert response.status_code == 404
