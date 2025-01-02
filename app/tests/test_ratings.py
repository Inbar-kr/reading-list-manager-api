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

test_rating_data = {
    "rating": 4,
    "user_feedback": "Great book!"
}

def create_book(client):
    response = client.post("/books/", json=test_book_data)
    assert response.status_code == 201, f"Book creation failed, expected 201 but got {response.status_code}"
    return response.json()["id"]

def create_rating_for_book(client, book_id, rating_data):
    response = client.post(f"/ratings/{book_id}", json=rating_data)
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
    return response.json()

def get_rating_for_book(client, book_id):
    response = client.get(f"/ratings/{book_id}")
    assert response.status_code == 200, "Failed to retrieve rating"
    return response.json()

def update_rating(client, rating_id, updated_data):
    response = client.put(f"/ratings/{rating_id}", json=updated_data)
    assert response.status_code == 200, "Rating update failed"
    return response.json()

def delete_rating_by_id(client, rating_id):
    response = client.delete(f"/ratings/{rating_id}")
    assert response.status_code == 204, "Rating deletion failed"
    return response

def test_create_rating(client):
    book_id = create_book(client)
    created_rating = create_rating_for_book(client, book_id, test_rating_data)
    assert created_rating["rating"] == test_rating_data["rating"], "Rating mismatch"
    assert created_rating["user_feedback"] == test_rating_data["user_feedback"], "User feedback mismatch"
    assert "id" in created_rating, "ID not returned"

def test_create_rating(client):
    book_id = create_book(client)
    created_rating = create_rating_for_book(client, book_id, test_rating_data)
    assert created_rating["rating"] == test_rating_data["rating"], "Rating mismatch"
    assert created_rating["user_feedback"] == test_rating_data["user_feedback"], "User feedback mismatch"
    assert "id" in created_rating, "ID not returned"

def test_update_rating(client):
    book_id = create_book(client)
    created_rating = create_rating_for_book(client, book_id, test_rating_data)
    rating_id = created_rating["id"]

    updated_data = {"rating": 5, "user_feedback": "Amazing book!"}
    updated_rating = update_rating(client, rating_id, updated_data)

    assert updated_rating["rating"] == updated_data["rating"], "Rating not updated correctly"
    assert updated_rating["user_feedback"] == updated_data["user_feedback"], "User feedback not updated"

def test_delete_rating(client):
    book_id = create_book(client)
    created_rating = create_rating_for_book(client, book_id, test_rating_data)
    rating_id = created_rating["id"]

    delete_rating_by_id(client, rating_id)

    response = client.get(f"/ratings/{book_id}")
    assert response.status_code == 404, "Failed to retrieve rating after deletion"
    assert response.json()["detail"] == "Rating not found", "Error message mismatch"

# Edge cases

def test_create_rating_invalid_rating(client):
    book_id = create_book(client)

    invalid_rating_data = {"rating": 0, "user_feedback": "Great book!"}
    response = client.post(f"/ratings/{book_id}", json=invalid_rating_data)
    assert response.status_code == 400, "Invalid rating (less than 1) did not return an error"

    invalid_rating_data = {"rating": 6, "user_feedback": "Great book!"}
    response = client.post(f"/ratings/{book_id}", json=invalid_rating_data)
    assert response.status_code == 400, "Invalid rating (greater than 5) did not return an error"


def test_update_rating_invalid_rating(client):
    book_id = create_book(client)

    create_response = client.post(f"/ratings/{book_id}", json=test_rating_data)
    assert create_response.status_code == 201, "Rating creation failed"
    created_rating = create_response.json()
    rating_id = created_rating["id"]

    invalid_update_data = {"rating": 0, "user_feedback": "Updated feedback"}
    update_response = client.put(f"/ratings/{rating_id}", json=invalid_update_data)
    assert update_response.status_code == 400, "Invalid rating update (less than 1) did not return an error"

    invalid_update_data = {"rating": 6, "user_feedback": "Updated feedback"}
    update_response = client.put(f"/ratings/{rating_id}", json=invalid_update_data)
    assert update_response.status_code == 400, "Invalid rating update (greater than 5) did not return an error"

def test_delete_non_existing_rating(client):
    response = client.delete(f"/ratings/99999")
    assert response.status_code == 404, "Delete non-existing rating did not return error"
    assert response.json()["detail"] == "Rating not found", "Error message mismatch"

def test_get_rating_for_non_existing_book(client):
    response = client.get(f"/ratings/99999")
    assert response.status_code == 404, "Get rating for non-existing book did not return error"
    assert response.json()["detail"] == "Rating not found", "Error message mismatch"
