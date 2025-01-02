from fastapi.testclient import TestClient
from app.tests.conftest import client
import pytest

# Test Data
test_book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "genre": "Fiction",
    "publication_year": 2018,
    "status_reading": "not_started"
}


# Utility Functions
def create_book(client, book_data):
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201, f"Book creation failed: {response.text}"  # Expecting 201 Created
    return response.json()["id"]

def get_book(client, book_id):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200, "Failed to retrieve book"
    return response.json()

def delete_book(client, book_id):
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204, "Failed to delete book"  # Expecting 204 No Content for successful deletion

# Tests
def test_create_book(client):
    book_id = create_book(client, test_book_data)
    data = get_book(client, book_id)
    assert data["title"] == test_book_data["title"], "Title mismatch"
    assert "id" in data, "ID not returned"

def test_get_book(client):
    book_id = create_book(client, test_book_data)
    data = get_book(client, book_id)
    for field, value in test_book_data.items():
        assert data[field] == value, f"{field} mismatch"

def test_get_books_list(client):
    # Create multiple books
    book_id_1 = create_book(client, test_book_data)
    test_book_data2 = {
        "title": "Another Test Book",
        "author": "Another Test Author",
        "genre": "Non-Fiction",
        "publication_year": 2020,
        "status_reading": "in_progress"
    }
    book_id_2 = create_book(client, test_book_data2)

    response = client.get("/books/")
    assert response.status_code == 200, "Failed to retrieve books list"
    books = response.json().get("books", [])

    titles = [book["title"] for book in books]
    assert test_book_data["title"] in titles, "First book not found in list"
    assert test_book_data2["title"] in titles, "Second book not found in list"

def test_update_book(client):
    book_id = create_book(client, test_book_data)
    updated_book_data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "genre": "Updated Fiction",
        "publication_year": 2022,
        "status_reading": "in_progress"
    }
    response = client.put(f"/books/{book_id}", json=updated_book_data)
    assert response.status_code == 200, "Failed to update book"

    updated_data = get_book(client, book_id)
    for field, value in updated_book_data.items():
        assert updated_data[field] == value, f"{field} mismatch"

def test_delete_book(client):
    book_id = create_book(client, test_book_data)
    delete_book(client, book_id)

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404, "Deleted book still found"

# Edge Cases
def test_create_book_missing_field(client):
    incomplete_data = {k: v for k, v in test_book_data.items() if k != "title"}
    response = client.post("/books/", json=incomplete_data)
    assert response.status_code == 422, "Book creation should fail with missing fields"

def test_create_book_invalid_data_type(client):
    invalid_data = {**test_book_data, "title": 123, "publication_year": "not_a_year"}
    response = client.post("/books/", json=invalid_data)
    assert response.status_code == 422, "Book creation should fail with invalid data types"

def test_get_nonexistent_book(client):
    response = client.get("/books/99999")
    assert response.status_code == 404, "Non-existent book should return 404"

def test_update_nonexistent_book(client):
    update_data = {**test_book_data, "title": "Updated"}
    response = client.put("/books/99999", json=update_data)
    assert response.status_code == 404, "Updating non-existent book should return 404"

def test_delete_nonexistent_book(client):
    response = client.delete("/books/99999")
    assert response.status_code == 404, "Deleting non-existent book should return 404"

def test_create_book_with_extra_fields(client):
    extra_data = {**test_book_data, "extra_field": "extra_value"}
    response = client.post("/books/", json=extra_data)
    assert response.status_code == 201, "Book creation should succeed with extra fields"  # Expecting 201
    data = response.json()
    assert "extra_field" not in data, "Extra fields should not be included in the response"

def test_update_book_invalid_fields(client):
    book_id = create_book(client, test_book_data)
    invalid_update_data = {"title": None, "publication_year": -1}
    response = client.put(f"/books/{book_id}", json=invalid_update_data)
    assert response.status_code == 422, "Update should fail with invalid data"
