USE reading_list_manager_schema;

-- Aggregations for reports

-- Average Rating by Genre
SELECT b.genre, AVG(r.rating) AS average_rating
FROM books b
LEFT JOIN Rating r ON b.id = r.book_id
GROUP BY b.genre
ORDER BY average_rating DESC;

-- Number of Books by Reading Status
SELECT b.status_reading, COUNT(*) AS book_count
FROM books b
GROUP BY b.status_reading
ORDER BY book_count DESC;

-- Most Popular Genre by Ratings Count
SELECT b.genre AS genre, COUNT(r.id) AS total_ratings
FROM books b
LEFT JOIN Rating r ON b.id = r.book_id
GROUP BY b.genre
ORDER BY total_ratings DESC
LIMIT 1;

-- Total Number of Books per Genre
SELECT genre, COUNT(*) AS total_books
FROM books
GROUP BY genre
ORDER BY total_books DESC;

-- Highest Rated Books
SELECT b.title AS title, b.author AS author, r.rating AS rating, r.user_feedback
FROM Books b
JOIN Rating r ON b.id = r.book_id
ORDER BY r.rating DESC
LIMIT 5;

-- Total Pages Read Across All Books
SELECT SUM(rp.current_page) AS total_pages_read
FROM ReadingProgress rp;

-- Genre with the Highest Reading Progress
SELECT b.genre AS genre,
ROUND(AVG((rp.current_page / rp.total_pages) * 100), 2) AS average_progress
FROM Books b
LEFT JOIN ReadingProgress rp ON b.id = rp.book_id
WHERE rp.total_pages > 0
GROUP BY b.genre
ORDER BY average_progress DESC
LIMIT 1;
