import json
import pytest
from app.api import crud


def test_create_note(test_app, monkeypatch):
    test_request_payload = {"title": "something", "description": "something else"}
    test_response_payload = {"id": 1, "title": "something", "description": "something else"}
    async def mock_post(payload):
        return 1

    monkeypatch.setattr(crud, "post", mock_post)

    response = test_app.post("/notes/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload
    
def test_read_note(test_app, monkeypatch):
    test_data = {"id": 1,"title": "something", "description": "something else"}
    
    async def mock_get(id):
        return test_data
    monkeypatch.setattr(crud,"get",mock_get)
    
    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert response.json() == test_data
    
def test_read_note(test_app, monkeypatch):
    async def mock_get(id):
        return None
    
    monkeypatch.setattr(crud, "get", mock_get)
    
    response = test_app.get("/notes/99")
    assert response.status_code == 404
    assert response.json()["detail"] ==  "Note not found"
 

def test_create_note_invalid_json(test_app):
    response = test_app.post("/notes/", data=json.dumps({"title": "something"}))
    assert response.status_code == 422