USE reading_list_manager_schema;

-- Joins Between Tables

-- Books with Ratings 
SELECT b.id, b.title, b.author, b.genre, b.publication_year, b.status_reading, 
	r.rating, r.user_feedback
FROM books b
LEFT JOIN rating r ON b.id = r.book_id
ORDER BY b.id;

-- Books with Progress
SELECT b.id, b.title, b.author, rp.current_page, rp.total_pages,
    (rp.current_page / rp.total_pages) * 100 AS percentage_completed
FROM books b
LEFT JOIN readingprogress rp ON b.id = rp.book_id
ORDER BY b.id;

-- Fetch Books with Notes
SELECT  b.id, b.title, b.author, n.notes_text, n.timestamp
FROM books b
LEFT JOIN notes n ON b.id = n.book_id
ORDER BY b.id;

-- Books with Ratings and Progress
SELECT b.id, b.title, b.author, b.genre, b.publication_year,
	r.rating, r.user_feedback,
    rp.current_page, rp.total_pages,
    (rp.current_page / rp.total_pages) * 100 AS percentage_completed
FROM books b
LEFT JOIN Rating r ON b.id = r.book_id
LEFT JOIN ReadingProgress rp ON b.id = rp.book_id
ORDER BY b.id;

-- Books with Ratings, Notes, and Favorites
SELECT b.id, b.title, b.author, b.genre, b.publication_year,
	r.rating, r.user_feedback,
    n.notes_text, n.timestamp,
    f.is_favorite
FROM books b
LEFT JOIN Rating r ON b.id = r.book_id
LEFT JOIN Notes n ON b.id = n.book_id
LEFT JOIN Favorites f ON b.id = f.book_id
ORDER BY b.id;

-- Books by Author with Ratings and Progress
SELECT b.id, b.title, b.author, b.genre, b.publication_year,
	r.rating, r.user_feedback,
    rp.current_page, rp.total_pages,
    (rp.current_page / rp.total_pages) * 100 AS percentage_completed
FROM books b
LEFT JOIN Rating r ON b.id = r.book_id
LEFT JOIN ReadingProgress rp ON b.id = rp.book_id
WHERE b.author = 'J.R.R. Tolkien'
ORDER BY b.title;

-- Fetch Books with All Associated Data
SELECT b.id, b.title, b.author, b.genre, b.publication_year,
	rp.current_page, rp.total_pages,
    (rp.current_page / rp.total_pages) * 100 AS percentage_completed,
    r.rating, r.user_feedback,
    n.notes_text, n.timestamp,
    f.is_favorite
FROM books b
LEFT JOIN ReadingProgress rp ON b.id = rp.book_id
LEFT JOIN Rating r ON b.id = r.book_id
LEFT JOIN Notes n ON b.id = n.book_id
LEFT JOIN Favorites f ON b.id = f.book_id
ORDER BY b.id;