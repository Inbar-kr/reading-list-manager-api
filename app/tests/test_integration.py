from fastapi.testclient import TestClient
import pytest
from app.tests.conftest import client

# Test Data
test_book_data = {
    "title": "Test Book",
    "author": "Test Author",
    "genre": "Fiction",
    "publication_year": 2021,
    "status_reading": "not_started"
}

test_note_data = {"notes_text": "This is a test note."}
test_progress_data = {"current_page": 100, "total_pages": 300}
test_rating_data = {"rating": 4, "user_feedback": "Excellent read!"}
test_favorite_data = {"is_favorite": True}

# Utility Functions
def create_book(client, book_data):
    response = client.post("/books/", json=book_data)
    assert response.status_code == 201, "Book creation failed"
    return response.json()["id"]

def create_note_for_book(client, book_id, note_data):
    response = client.post(f"/notes/{book_id}", json=note_data)
    assert response.status_code == 201, "Note creation failed"
    return response.json()

def create_reading_progress(client, book_id, progress_data):
    response = client.post(f"/progress/{book_id}", json=progress_data)
    assert response.status_code == 201, "Reading progress creation failed"
    return response.json()

def create_rating_for_book(client, book_id, rating_data):
    response = client.post(f"/ratings/{book_id}", json=rating_data)
    assert response.status_code == 201, "Rating creation failed"
    return response.json()

def create_favorite_for_book(client, book_id, favorite_data):
    response = client.post(f"/favorites/{book_id}", json=favorite_data)
    assert response.status_code == 201, "Marking book as favorite failed"
    return response.json()

def get_book(client, book_id):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200, "Failed to retrieve book"
    return response.json()

def get_notes_for_book(client, book_id):
    response = client.get(f"/notes/{book_id}")
    assert response.status_code == 200, "Failed to retrieve notes"
    return response.json()

def get_reading_progress(client, book_id):
    response = client.get(f"/progress/{book_id}")
    assert response.status_code == 200, "Failed to retrieve reading progress"
    return response.json()

def get_rating_for_book(client, book_id):
    response = client.get(f"/ratings/{book_id}")
    assert response.status_code == 200, "Failed to retrieve rating"
    return response.json()

def get_favorite_status(client, book_id):
    response = client.get(f"/favorites/{book_id}")
    assert response.status_code == 200, "Failed to retrieve favorite status"
    return response.json()

# Integration Test
def test_full_integration(client):
    # Step 1: Create a Book
    book_id = create_book(client, test_book_data)

    # Step 2: Add a Note to the Book
    created_note = create_note_for_book(client, book_id, test_note_data)
    assert created_note["notes_text"] == test_note_data["notes_text"], "Notes text mismatch"

    # Step 3: Track Reading Progress for the Book
    created_progress = create_reading_progress(client, book_id, test_progress_data)
    assert created_progress["current_page"] == test_progress_data["current_page"], "Current page mismatch"
    assert created_progress["total_pages"] == test_progress_data["total_pages"], "Total pages mismatch"

    # Step 4: Rate the Book
    created_rating = create_rating_for_book(client, book_id, test_rating_data)
    assert created_rating["rating"] == test_rating_data["rating"], "Rating mismatch"
    assert created_rating["user_feedback"] == test_rating_data["user_feedback"], "User feedback mismatch"

    # Step 5: Mark the Book as Favorite
    created_favorite = create_favorite_for_book(client, book_id, test_favorite_data)
    assert created_favorite["is_favorite"] == test_favorite_data["is_favorite"], "Favorite status mismatch"

    # Step 6: Retrieve and Verify the Book's Data
    retrieved_book = get_book(client, book_id)
    assert retrieved_book["title"] == test_book_data["title"], "Book title mismatch"
    assert retrieved_book["author"] == test_book_data["author"], "Book author mismatch"

    # Step 7: Verify the Note
    notes_response = get_notes_for_book(client, book_id)
    notes = notes_response.get("notes", [])
    assert len(notes) > 0, "No notes found for the book"
    assert notes[0]["notes_text"] == test_note_data["notes_text"], "Notes text mismatch"

    # Step 8: Verify the Reading Progress
    reading_progress = get_reading_progress(client, book_id)
    assert reading_progress["current_page"] == test_progress_data["current_page"], "Current page mismatch"
    assert reading_progress["total_pages"] == test_progress_data["total_pages"], "Total pages mismatch"

    # Step 9: Verify the Rating
    rating = get_rating_for_book(client, book_id)
    assert rating["rating"] == test_rating_data["rating"], "Rating mismatch"
    assert rating["user_feedback"] == test_rating_data["user_feedback"], "User feedback mismatch"

    # Step 10: Verify the Favorite Status
    favorite = get_favorite_status(client, book_id)
    assert favorite["is_favorite"] == test_favorite_data["is_favorite"], "Favorite status mismatch"
