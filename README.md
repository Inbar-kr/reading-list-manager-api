# Reading List Manager

## Project Overview

Reading List Manager is a backend application built with FastAPI and SQLAlchemy that allows users to track and manage their reading lists. 
It provides functionality for adding, updating, deleting, and viewing books. 
In addition, it allows users to track their reading progress, add notes, rate books, and mark favorites.

## Key Features

* **Books:** Manage details of books, including title, author, genre, and publication year.
* **Reading Progress:** Track progress by marking the current page and calculating the percentage completed.
* **Notes:** Add, edit, and view notes related to each book.
* **Ratings:** Rate books from 1 to 5 and add feedback.
* **Favorites:** Mark books as favorites.

## Tech Stack

* **Backend Framework:** FastAPI
* **Database:** MySQL (or SQLite, depending on configuration)
* **ORM:** SQLAlchemy
* **Pydantic:** For data validation
* **Testing:** Pytest (for unit, integration and E2E flow tests)
* **Database Migration Tool**: Alembic (for database schema migrations)
* **API Documentation:** Automatic Swagger UI generated by FastAPI

## Prerequisites

Before you begin, ensure you have the following installed:

* Python 3.7 or higher
* MySQL (or SQLite)
* Virtual Environment (optional but recommended)

## Installation
1. Clone the repository:
[git clone](https://github.com/Inbar-kr/reading-list-manager-api.git)

    `cd reading-list-manager`
2. Create and activate a virtual environment (optional but recommended):

    For Windows:
   ` python -m venv venv`
   `.\venv\Scripts\activate`

    For macOS/Linux:
    `python3 -m venv venv`
   `source venv/bin/activate`

3. Install dependencies:
    `pip install -r requirements.txt`

4.  Set up the database:
    Create a new database named reading_list_manager_schema

5. Running the Application:

    To run the FastAPI application, use Uvicorn:
    `uvicorn app.main:app --reload`

By default, the API will be available at http://localhost:8000.

* Open Swagger UI at http://localhost:8000/docs to view the available endpoints and interact with the API.
* The Redoc documentation is available at http://localhost:8000/redoc.

## Endpoints
**Books Endpoints:**
* GET /books: Get a list of all books.
* POST /books: Create a new book.
* GET /books/{book_id}: Get details of a specific book.
* PUT /books/{book_id}: Update a specific book.
* DELETE /books/{book_id}: Delete a specific book.

**Reading Progress Endpoints:**
* GET /progress/{book_id}: Get the reading progress for a specific book.
* POST /progress/{book_id}: Set or update reading progress for a book.

**Notes Endpoints:**
* GET /notes/{book_id}: Get all notes for a specific book.
* POST /notes/{book_id}: Add a new note for a book.

**Ratings Endpoints:**
* GET /ratings/{book_id}: Get the rating and feedback for a book.
* POST /ratings/{book_id}: Submit a rating for a book.

**Favorites Endpoints:**
* GET /favorites/{book_id}: Check if a book is marked as a favorite.
* POST /favorites/{book_id}: Mark a book as a favorite or remove it from favorites.

## Running Tests
To run the tests for the project (Tests are located in the app/tests/ folder), ensure you have pytest installed:
`pip install pytest`

Then, run the tests: `pytest`

###### Note: This project is a personal and educational portfolio project. It is not intended for redistribution or external use.