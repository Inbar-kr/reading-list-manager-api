from fastapi.testclient import TestClient
from app.tests.conftest import client
from app.main import app
import pytest

test_book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "genre": "Fiction",
    "publication_year": 2021,
    "status_reading": "not_started"
}

test_favorite_data = {
    "is_favorite": True
}

def create_book(client):
    response = client.post("/books/", json=test_book_data)
    assert response.status_code == 201, "Book creation failed"
    return response.json()["id"]

def create_favorite_for_book(client, book_id, favorite_data):
    response = client.post(f"/favorites/{book_id}", json=favorite_data)
    assert response.status_code == 201, "Marking book as favorite failed"
    return response.json()

def get_favorite_status(client, book_id):
    response = client.get(f"/favorites/{book_id}")
    return response

def update_favorite_status(client, favorite_id, updated_data):
    response = client.put(f"/favorites/{favorite_id}", json=updated_data)
    return response

def delete_favorite_status(client, favorite_id):
    response = client.delete(f"/favorites/{favorite_id}")
    return response

def test_mark_book_as_favorite(client):
    book_id = create_book(client)
    favorite = create_favorite_for_book(client, book_id, test_favorite_data)

    assert favorite["is_favorite"] == test_favorite_data["is_favorite"], "Favorite status mismatch"
    assert favorite["book_id"] == book_id, "Book ID mismatch"

def test_get_favorite_status(client):
    book_id = create_book(client)
    create_favorite_for_book(client, book_id, test_favorite_data)

    response = get_favorite_status(client, book_id)
    favorite = response.json()
    assert response.status_code == 200, "Failed to retrieve favorite status"
    assert favorite["is_favorite"] == test_favorite_data["is_favorite"], "Favorite status mismatch"
    assert favorite["book_id"] == book_id, "Book ID mismatch"

def test_update_favorite_status(client):
    book_id = create_book(client)
    create_favorite_for_book(client, book_id, test_favorite_data)

    updated_favorite_data = {"is_favorite": False}
    response = update_favorite_status(client, book_id, updated_favorite_data)
    updated_favorite = response.json()

    assert response.status_code == 200, "Updating favorite status failed"
    assert updated_favorite["is_favorite"] == updated_favorite_data["is_favorite"], "Favorite status update mismatch"
    assert updated_favorite["book_id"] == book_id, "Book ID mismatch"

def test_delete_favorite_status(client):
    book_id = create_book(client)
    post_response = create_favorite_for_book(client, book_id, test_favorite_data)
    favorite_id = post_response["id"]

    response = delete_favorite_status(client, favorite_id)
    assert response.status_code == 204, "Deleting favorite status failed"

    retrieve_response = get_favorite_status(client, book_id)
    assert retrieve_response.status_code == 404, "Favorite status not properly deleted"

# Edge Cases

def test_mark_favorite_invalid_book_id(client):
    invalid_book_id = 999999
    response = client.post(f"/favorites/{invalid_book_id}", json=test_favorite_data)
    assert response.status_code == 404, "Expected 404 for invalid book ID"
    assert response.json()["detail"] == "Book not found", "Incorrect error message for invalid book ID"

def test_mark_favorite_invalid_data(client):
    book_id = create_book(client)
    invalid_favorite_data = {"is_favorite": "not_a_boolean"}
    response = client.post(f"/favorites/{book_id}", json=invalid_favorite_data)
    assert response.status_code == 422, "Expected 422 for invalid data type"
    assert "Input should be a valid boolean" in response.json()["detail"][0][
        "msg"], "Incorrect validation error message"

def test_update_favorite_invalid_id(client):
    book_id = create_book(client)
    post_response = create_favorite_for_book(client, book_id, test_favorite_data)
    favorite_id = post_response["id"]

    invalid_favorite_id = 999999
    updated_favorite_data = {"is_favorite": False}
    response = update_favorite_status(client, invalid_favorite_id, updated_favorite_data)
    assert response.status_code == 404, "Expected 404 for invalid favorite ID"
    assert response.json()["detail"] == "Favorite status not found", "Incorrect error message for invalid favorite ID"

def test_delete_favorite_invalid_id(client):
    book_id = create_book(client)
    post_response = create_favorite_for_book(client, book_id, test_favorite_data)
    favorite_id = post_response["id"]

    invalid_favorite_id = 999999
    response = delete_favorite_status(client, invalid_favorite_id)
    assert response.status_code == 404, "Expected 404 for invalid favorite ID"
    assert response.json()["detail"] == "Favorite status not found", "Incorrect error message for invalid favorite ID"

def test_get_favorite_status_not_found(client):
    invalid_book_id = 999999
    response = client.get(f"/favorites/{invalid_book_id}")
    assert response.status_code == 404, "Expected 404 for non-existent favorite status"
    assert response.json()["detail"] == "Favorite status not found", "Incorrect error message for non-existent favorite status"
