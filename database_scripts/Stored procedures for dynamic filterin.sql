USE reading_list_manager_schema;

-- Stored Procedure

-- Filter Books by Genre and Author

DELIMITER $$

CREATE PROCEDURE FilterBooksByGenreAuthor(
    IN genre_filter VARCHAR(50),
    IN author_filter VARCHAR(100)
)
BEGIN
    SELECT b.id, b.title, b.author, b.genre, b.publication_year, b.status_reading
    FROM Books b
    WHERE 
        (genre_filter IS NULL OR b.genre = genre_filter)
        AND (author_filter IS NULL OR b.author LIKE CONCAT('%', author_filter, '%'))
    ORDER BY 
        b.title;
END $$

DELIMITER ;

CALL FilterBooksByGenreAuthor('Fantasy', 'Tolkien');
CALL FilterBooksByGenreAuthor('Fantasy', NULL);

-- DROP PROCEDURE IF EXISTS FilterBooksByGenreAuthor;

-- Filter Books by Reading Status

DELIMITER $$

CREATE PROCEDURE FilterBooksByStatusAndGenre(
    IN status_filter VARCHAR(50),
    IN genre_filter VARCHAR(50)
)
BEGIN
    SELECT b.id, b.title, b.author, b.genre, b.publication_year, b.status_reading
    FROM Books b
    WHERE 
        (status_filter IS NULL OR b.status_reading = status_filter)
        AND (genre_filter IS NULL OR b.genre = genre_filter)
    ORDER BY b.title;
END $$

DELIMITER ;

CALL FilterBooksByStatusAndGenre('not_started', 'Fantasy');
CALL FilterBooksByStatusAndGenre('not_started', NULL);


-- Filter Books by Rating and Author
DELIMITER $$

CREATE PROCEDURE FilterBooksByRatingAndAuthor(
    IN min_rating INT,
    IN author_filter VARCHAR(100)
)
BEGIN
    SELECT b.id, b.title, b.author, b.genre, b.publication_year, r.rating, r.user_feedback
    FROM Books b
    JOIN Rating r ON b.id = r.book_id
    WHERE r.rating >= min_rating
        AND (author_filter IS NULL OR b.author LIKE CONCAT('%', author_filter, '%'))
    ORDER BY r.rating DESC;
END $$

DELIMITER ;

CALL FilterBooksByRatingAndAuthor(4, 'Tolkien');

-- Filter Books by Progress

DELIMITER $$

CREATE PROCEDURE FilterBooksByProgress(
    IN min_percentage DECIMAL(5,2),
    IN max_percentage DECIMAL(5,2)
)
BEGIN
    SELECT 
        b.id, b.title, b.author, b.genre, b.publication_year, rp.current_page, rp.total_pages,
        (rp.current_page / rp.total_pages) * 100 AS percentage_completed
    FROM Books b
    JOIN ReadingProgress rp ON b.id = rp.book_id
    WHERE (rp.current_page / rp.total_pages) * 100 BETWEEN min_percentage AND max_percentage
    ORDER BY percentage_completed DESC;
END $$

DELIMITER ;

CALL FilterBooksByProgress(20, 75);

-- Fetch All Books with Dynamic Filters

DELIMITER $$

CREATE PROCEDURE FetchBooksWithDynamicFilters(
    IN status_filter VARCHAR(50),
    IN genre_filter VARCHAR(50),
    IN author_filter VARCHAR(100)
)
BEGIN
    SELECT b.id, b.title, b.author, b.genre, b.publication_year, b.status_reading
    FROM Books b
    WHERE (status_filter IS NULL OR b.status_reading = status_filter)
        AND (genre_filter IS NULL OR b.genre = genre_filter)
        AND (author_filter IS NULL OR b.author LIKE CONCAT('%', author_filter, '%'))
    ORDER BY b.title;
END $$

DELIMITER ;

CALL FetchBooksWithDynamicFilters('completed', 'Fantasy', 'Rowling');

-- Update Status to "Completed"

DELIMITER $$

CREATE TRIGGER UpdateStatusOnCompletion
AFTER UPDATE ON ReadingProgress
FOR EACH ROW
BEGIN
    IF NEW.current_page = NEW.total_pages THEN
        UPDATE Books
        SET status_reading = 'completed'
        WHERE id = NEW.book_id;
    END IF;
END $$

DELIMITER ;

    
    

