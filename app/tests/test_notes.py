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

test_note_data = {
    "notes_text": "This is a test note for the book."
}

def create_book(client):
    response = client.post("/books/", json=test_book_data)
    assert response.status_code == 201, "Book creation failed"
    return response.json()["id"]


def create_note_for_book(client, book_id, note_data):
    response = client.post(f"/notes/{book_id}", json=note_data)
    assert response.status_code == 201, "Note creation failed"
    return response.json()

def get_notes_for_book(client, book_id):
    response = client.get(f"/notes/{book_id}")
    assert response.status_code == 200, "Failed to retrieve notes"
    return response.json()["notes"]

def delete_note_by_id(client, note_id):
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204, "Note deletion failed"
    return response.json()

def test_create_note(client):
    book_id = create_book(client)
    created_note = create_note_for_book(client, book_id, test_note_data)
    assert created_note["notes_text"] == test_note_data["notes_text"], "Notes text mismatch"
    assert "id" in created_note, "ID not returned"

def test_get_notes(client):
    book_id = create_book(client)
    create_note_for_book(client, book_id, test_note_data)
    notes = get_notes_for_book(client, book_id)
    assert len(notes) > 0, "No notes found"
    assert notes[0]["notes_text"] == test_note_data["notes_text"], "Notes text mismatch"


def test_delete_note(client):
    book_id = create_book(client)
    created_note = create_note_for_book(client, book_id, test_note_data)
    note_id = created_note["id"]

    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 204, "Note deletion failed"

    response = client.get(f"/notes/{book_id}")
    notes = response.json()["notes"]
    assert not any(note["id"] == note_id for note in notes), "Deleted note still exists"


# Edge cases
def test_create_note_for_non_existent_book(client):
    non_existent_book_id = 99999
    response = client.post(f"/notes/{non_existent_book_id}", json=test_note_data)
    assert response.status_code == 404, "Expected 404 when trying to create a note for a non-existent book"
    assert response.json()["detail"] == "Book not found", "Incorrect error message"

def test_create_note_with_missing_notes_text(client):
    book_id = create_book(client)
    invalid_note_data = {"notes_text": ""}
    response = client.post(f"/notes/{book_id}", json=invalid_note_data)
    assert response.status_code == 422, "Expected 422 when note text is empty"
    assert "detail" in response.json(), "Expected validation error message"

def test_get_notes_for_non_existent_book(client):
    non_existent_book_id = 9999
    response = client.get(f"/notes/{non_existent_book_id}")
    assert response.status_code == 404, "Expected 404 when retrieving notes for a non-existent book"
    assert response.json()["detail"] == "Book not found", "Incorrect error message"

def test_delete_non_existent_note(client):
    non_existent_note_id = 9999
    response = client.delete(f"/notes/{non_existent_note_id}")
    assert response.status_code == 404, "Expected 404 when trying to delete a non-existent note"
    assert response.json()["detail"] == "Note not found", "Incorrect error message"


def test_delete_note_after_deletion(client):
    book_id = create_book(client)
    created_note = create_note_for_book(client, book_id, test_note_data)
    note_id = created_note["id"]

    delete_response = client.delete(f"/notes/{note_id}")
    assert delete_response.status_code == 204, "Expected 204 after deleting the note"

    delete_response_again = client.delete(f"/notes/{note_id}")
    assert delete_response_again.status_code == 404, "Expected 404 when deleting a note that is already deleted"
    assert delete_response_again.json()["detail"] == "Note not found", "Incorrect error message"


def test_get_notes_with_skip_and_limit(client):
    book_id = create_book(client)

    for i in range(5):
        create_note_for_book(client, book_id, {"notes_text": f"Note {i+1}"})

    response = client.get(f"/notes/{book_id}?skip=5&limit=2")
    assert response.status_code == 200, "Failed to retrieve notes with skip and limit"
    notes = response.json()["notes"]
    assert len(notes) == 0, "Expected no notes when skip exceeds total notes"
