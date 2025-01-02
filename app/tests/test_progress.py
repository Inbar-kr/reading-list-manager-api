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

test_progress_data = {
    "current_page": 50,
    "total_pages": 300
}


def create_book(client, book_data):
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201, "Book creation failed"
    return response.json()["id"]


def create_reading_progress(client, book_id, progress_data):
    progress_response = client.post(f"/progress/{book_id}", json=progress_data)
    assert progress_response.status_code == 201, "Reading progress creation failed"
    progress = progress_response.json()
    assert "id" in progress, "ID not returned"
    return progress


def update_reading_progress(client, progress_id, updated_data):
    update_response = client.put(f"/progress/{progress_id}", json=updated_data)
    assert update_response.status_code == 200, "Reading progress update failed"
    updated_progress = update_response.json()
    assert "id" in updated_progress, "ID not returned"
    return updated_progress


def retrieve_reading_progress(client, book_id):
    retrieve_response = client.get(f"/progress/{book_id}")
    assert retrieve_response.status_code == 200, "Failed to retrieve reading progress"
    return retrieve_response.json()


def delete_reading_progress(client, progress_id):
    delete_response = client.delete(f"/progress/{progress_id}")
    assert delete_response.status_code == 204, "Reading progress deletion failed"
    return delete_response


def test_create_reading_progress(client):
    book_id = create_book(client, test_book_data)
    progress = create_reading_progress(client, book_id, test_progress_data)
    assert progress["current_page"] == test_progress_data["current_page"], "Current page mismatch"
    assert progress["total_pages"] == test_progress_data["total_pages"], "Total pages mismatch"


def test_get_reading_progress(client):
    book_id = create_book(client, test_book_data)
    create_reading_progress(client, book_id, test_progress_data)

    retrieved_progress = retrieve_reading_progress(client, book_id)
    assert retrieved_progress["current_page"] == test_progress_data["current_page"], "Current page mismatch"
    assert retrieved_progress["total_pages"] == test_progress_data["total_pages"], "Total pages mismatch"


def test_update_reading_progress(client):
    book_id = create_book(client, test_book_data)
    progress = create_reading_progress(client, book_id, test_progress_data)

    updated_progress_data = {
        "current_page": 150,
        "total_pages": 300
    }
    updated_progress = update_reading_progress(client, progress["id"], updated_progress_data)

    retrieved_progress = retrieve_reading_progress(client, book_id)
    assert retrieved_progress["current_page"] == updated_progress_data["current_page"], "Updated current page mismatch"
    assert retrieved_progress["total_pages"] == updated_progress_data["total_pages"], "Updated total pages mismatch"


def test_delete_reading_progress(client):
    book_id = create_book(client, test_book_data)
    progress = create_reading_progress(client, book_id, test_progress_data)

    delete_response = delete_reading_progress(client, progress["id"])
    assert delete_response.status_code == 204, "Reading progress deletion failed"

    retrieve_response = client.get(f"/progress/{book_id}")
    assert retrieve_response.status_code == 404, "Deleted progress should not be retrievable"
    assert retrieve_response.json()["detail"] == "Progress not found", "Incorrect error message"


# Edge Cases

def test_update_progress_invalid_progress_id(client):
    invalid_progress_id = 999999
    response = client.put(f"/progress/{invalid_progress_id}", json={"current_page": 50, "total_pages": 100})
    assert response.status_code == 404, "Progress update did not return 404 for invalid progress ID"

def test_update_progress_boundary_values(client):
    book_id = create_book(client, test_book_data)

    progress_data = {
        "current_page": 50,
        "total_pages": 300
    }
    progress = create_reading_progress(client, book_id, progress_data)

    # Update progress to 0%
    update_response = client.put(f"/progress/{progress['id']}", json={"current_page": 0, "total_pages": 300})
    assert update_response.status_code == 200, "Failed to update progress to 0%"
    updated_progress = update_response.json()
    assert updated_progress["current_page"] == 0, "Progress not set to 0%"

    # Update progress to 100%
    update_response = client.put(f"/progress/{progress['id']}", json={"current_page": 300, "total_pages": 300})
    assert update_response.status_code == 200, "Failed to update progress to 100%"
    updated_progress = update_response.json()
    assert updated_progress["current_page"] == 300, "Progress not set to 100%"


def test_update_progress_negative_value(client):
    book_id = create_book(client, test_book_data)

    response = client.put(f"/progress/{book_id}", json={"current_page": -10})
    assert response.status_code == 422, "Negative progress value should return a 422 status"
    assert "detail" in response.json(), "Error detail should be present"
    assert "current_page" in response.json()["detail"], "Error should mention current_page"


def test_get_progress_invalid_book_id(client):
    invalid_book_id = 999999
    response = client.get(f"/progress/{invalid_book_id}")
    assert response.status_code == 404, "Fetching progress for invalid book ID should return 404"
