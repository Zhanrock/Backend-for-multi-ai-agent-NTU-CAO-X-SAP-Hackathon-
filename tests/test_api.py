# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ask_arai():
    response = client.post("/ask_arai", json={
        "question": "What is FAN?",
        "style": "bullet"
    })
    assert response.status_code == 200
    assert "answer" in response.json()

def test_kai_ideas():
    response = client.get("/kai/ideas")
    assert response.status_code == 200
    assert "ideas" in response.json()
