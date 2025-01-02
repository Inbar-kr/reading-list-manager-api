from app.main import app
import pytest

# Test Data
test_book_data = {
    "title": "E2E Test Book",
    "author": "E2E Test Author",
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

def add_note_to_book(client, book_id, note_data):
    response = client.post(f"/notes/{book_id}", json=note_data)
    assert response.status_code == 201, "Failed to add note"
    return response.json()

def track_reading_progress(client, book_id, progress_data):
    response = client.post(f"/progress/{book_id}", json=progress_data)
    assert response.status_code == 201, "Failed to track progress"
    return response.json()

def add_rating_to_book(client, book_id, rating_data):
    response = client.post(f"/ratings/{book_id}", json=rating_data)
    assert response.status_code == 201, "Failed to add rating"
    return response.json()

def mark_as_favorite(client, book_id, favorite_data):
    response = client.post(f"/favorites/{book_id}", json=favorite_data)
    assert response.status_code == 201, "Failed to mark as favorite"
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
    assert response.status_code == 200, "Failed to retrieve progress"
    return response.json()

def get_rating_for_book(client, book_id):
    response = client.get(f"/ratings/{book_id}")
    assert response.status_code == 200, "Failed to retrieve rating"
    return response.json()

def get_favorite_status(client, book_id):
    response = client.get(f"/favorites/{book_id}")
    assert response.status_code == 200, "Failed to retrieve favorite status"
    return response.json()

# E2E Test Workflow
@pytest.mark.usefixtures("client")
def test_full_e2e_workflow(client):
    # Step 1: Add a New Book
    book_id = create_book(client, test_book_data)

    # Step 2: Add Notes to the Book
    added_note = add_note_to_book(client, book_id, test_note_data)
    assert added_note["notes_text"] == test_note_data["notes_text"], "Notes text mismatch"

    # Step 3: Track Reading Progress
    progress = track_reading_progress(client, book_id, test_progress_data)
    assert progress["current_page"] == test_progress_data["current_page"], "Progress page mismatch"

    # Step 4: Add a Rating for the Book
    rating = add_rating_to_book(client, book_id, test_rating_data)
    assert rating["rating"] == test_rating_data["rating"], "Rating mismatch"

    # Step 5: Mark the Book as Favorite
    favorite = mark_as_favorite(client, book_id, test_favorite_data)
    assert favorite["is_favorite"] == test_favorite_data["is_favorite"], "Favorite status mismatch"

    # Step 6: Fetch and Verify the Book's Data
    book = get_book(client, book_id)
    assert book["title"] == test_book_data["title"], "Book title mismatch"
    assert book["author"] == test_book_data["author"], "Book author mismatch"

    # Step 7: Fetch and Verify the Notes
    notes = get_notes_for_book(client, book_id)
    assert len(notes["notes"]) > 0, "No notes found for the book"
    assert notes["notes"][0]["notes_text"] == test_note_data["notes_text"], "Notes text mismatch"

    # Step 8: Fetch and Verify the Reading Progress
    progress = get_reading_progress(client, book_id)
    assert progress["current_page"] == test_progress_data["current_page"], "Reading progress page mismatch"
    assert progress["total_pages"] == test_progress_data["total_pages"], "Total pages mismatch"

    # Step 9: Fetch and Verify the Rating
    rating = get_rating_for_book(client, book_id)
    assert rating["rating"] == test_rating_data["rating"], "Rating mismatch"
    assert rating["user_feedback"] == test_rating_data["user_feedback"], "User feedback mismatch"

    # Step 10: Fetch and Verify the Favorite Status
    favorite = get_favorite_status(client, book_id)
    assert favorite["is_favorite"] == test_favorite_data["is_favorite"], "Favorite status mismatch"
