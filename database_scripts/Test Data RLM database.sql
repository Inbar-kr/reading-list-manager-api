USE reading_list_manager_schema;


INSERT INTO Books (title, author, genre, publication_year, status_reading)
VALUES
('Fourth Wing', 'Rebecca Yarros', 'Fantasy', 2023, 'not_started'),
('A Court of Thorns and Roses', 'Sarah J. Maas', 'Fantasy', 2015, 'in_progress'),
('The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 1954, 'completed'),
('The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 'Fantasy', 1950, 'not_started'),
('Harry Potter and the Prisoner of Azkaban', 'J.K. Rowling', 'Fantasy', 1999, 'completed'),
('Beach Read', 'Emily Henry', 'Romance', 2020, 'in_progress'),
('Pride and Prejudice', 'Jane Austen', 'Romance', 1813, 'not_started'),
('The Housemaid', 'Freida McFadden', 'Thriller', 2022, 'completed'),
('Friends, Lovers, and the Big Terrible Thing', 'Matthew Perry', 'Memoir', 2022, 'in_progress'),
('Outlander', 'Diana Gabaldon', 'Historical Fiction', 1991, 'completed'),
('The Song of Achilles', 'Madeline Miller', 'Fantasy', 2011, 'not_started'),
('House of Flame and Shadow', 'Sarah J. Maas', 'Fantasy', 2024, 'not_started'),
('Where the Crawdads Sing', 'Delia Owens', 'Mystery', 2018, 'completed'),
('The Silent Patient', 'Alex Michaelides', 'Thriller', 2019, 'not_started'),
('Normal People', 'Sally Rooney', 'Romance', 2018, 'in_progress'),
('The Night Circus', 'Erin Morgenstern', 'Fantasy', 2011, 'completed'),
('Big Little Lies', 'Liane Moriarty', 'Mystery', 2014, 'not_started'),
('The Midnight Library', 'Matt Haig', 'Fantasy', 2020, 'in_progress'),
('Quicksilver', 'Callie Hart', 'Thriller', 2023, 'in_progress'),
('The Invisible Life of Addie LaRue', 'V.E. Schwab', 'Fantasy', 2020, 'not_started'),
('The Hating Game', 'Sally Thorne', 'Romance', 2016, 'completed'),
('All Rhodes Lead Here', 'Mariana Zapata', 'Romance', 2023, 'completed'),
('A Little Life', 'Hanya Yanagihara', 'Drama', 2015, 'completed'),
('The Four Winds', 'Kristin Hannah', 'Historical Fiction', 2021, 'in_progress'),
('Verity', 'Colleen Hoover', 'Romance', 2018, 'completed');


INSERT INTO Rating (book_id, rating, user_feedback)
VALUES
(2, 5, 'Loved it! One of the best fantasy books I have read.'),
(3, 5, 'A classic! Timeless masterpiece. Highly recommend.'),
(5, 5, 'A fantastic book in the Harry Potter series. My favorite of the three.'),
(6, 4, 'Not my favorite, but I can appreciate the character depth and humor.'),
(8, 5, 'Gripping from the beginning! Can’t wait to see where it goes.'),
(9, 4, 'It’s a memoir, so it’s a bit slow, but definitely heartfelt and funny.'), 
(10, 5, 'I adore this book. So much history and emotion packed into one story.'), 
(13, 4, 'Not what I was expecting, but definitely intriguing.'),
(15, 4, 'The romance was deep, I couldn’t stop thinking about it after finishing.'),
(16, 5, 'Such a magical, atmospheric book. Love the mystery and characters!'),
(18, 5, 'Such a beautifully written, touching book. A must-read.'),
(19, 4, 'The suspense keeps building! I’m loving this thriller.'),
(21, 4, 'A sweet romance, definitely one for fans of the genre.'),
(22, 5, 'Absolutely in love with this one! Can’t stop thinking about it.'),
(23, 5, 'A beautiful, heartbreaking journey. Couldn’t put it down.'),
(24, 4, 'A powerful read. Glad I finished it, but emotionally drained.'),
(25, 4, 'The ending was predictable, but I still really enjoyed the ride.');


INSERT INTO ReadingProgress (book_id, current_page, total_pages)
VALUES
(1, 0, 517),
(2, 200, 419),
(3, 1216, 1216),
(4, 100, 206),
(5, 500, 500),
(6, 150, 350),
(7, 50, 350),
(8, 329, 329),
(9, 150, 350),
(10, 500, 500),
(11, 0, 408),
(12, 0, 835),
(13, 384, 384),
(14, 0, 336),
(15, 73, 273),
(16, 506, 506),
(17, 0, 460),
(18, 150, 288),
(19, 217, 624),
(20, 0, 448),
(21, 365, 365),
(22, 572, 572),
(23, 720, 720),
(24, 237, 464),
(25, 336, 336);


INSERT INTO Notes (book_id, notes_text, timestamp) 
VALUES
(3, 'A timeless classic! The depth of the story and its characters is unmatched. An unforgettable journey through Middle-earth.', NOW()),
(5, 'Absolutely loved this book! The story continues to captivate, and the character development is fantastic. One of my all-time favorites.', NOW()),
(8, 'A thrilling read from start to finish! The twists and turns kept me on the edge of my seat. Definitely a must-read for thriller fans.', NOW()),
(10, 'Such an emotional ride! The mix of history, romance, and passion made this book hard to put down. A beautiful journey.', NOW()),
(13, 'A haunting and beautifully written novel. The imagery and atmosphere were unforgettable, and the characters were so real and vivid.', NOW()),
(16, 'What a masterpiece! Magical, mysterious, and utterly captivating. I couldn’t stop thinking about it long after I finished it.', NOW()),
(21, 'Such a sweet, heartwarming romance. The chemistry between the characters was incredible, and I really enjoyed the dynamic between them.', NOW()),
(22, 'Absolutely loved this one! It was so heartfelt and beautifully written. A slow-burn romance with great depth and emotion.', NOW()),
(23, 'A heartbreaking and poignant story. I couldn’t put it down. The writing is brilliant, and the character arcs are deeply moving.', NOW()),
(25, 'The story was gripping from beginning to end. Despite the predictable ending, I really enjoyed the emotional rollercoaster.', NOW());


INSERT INTO Favorites (book_id, is_favorite)
VALUES
(3, TRUE),
(5, TRUE),
(8, TRUE),
(10, TRUE),
(13, TRUE),
(16, TRUE),
(21, TRUE),
(22, TRUE),
(23, TRUE),
(25, TRUE);
