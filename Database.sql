CREATE DATABASE library_system;

USE library_system;

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'Available'
);

 select * from books;
 
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

 select * from users;

SHOW CREATE TABLE books;

CREATE TABLE issued_books (
  issue_id INT AUTO_INCREMENT PRIMARY KEY,
  book_id INT,
  borrower_name VARCHAR(255),
  issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE issued_books ADD COLUMN due_date DATE;
select * from issued_books;


DELIMITER //

-- Trigger to set status to 'issued' when a book is issued
CREATE TRIGGER after_issue_insert
AFTER INSERT ON issued_books
FOR EACH ROW
BEGIN
    UPDATE books SET status = 'issued' WHERE book_id = NEW.book_id;
END;
//
DELIMITER //
-- Trigger to set status to 'available' when a book is returned
CREATE TRIGGER after_issue_delete
AFTER DELETE ON issued_books
FOR EACH ROW
BEGIN
    UPDATE books SET status = 'available' WHERE book_id = OLD.book_id;
END;
//

DELIMITER ;

DELIMITER //

DELIMITER //

CREATE PROCEDURE issue_book(
    IN p_book_id INT,
    IN p_borrower_name VARCHAR(55) )
BEGIN
    INSERT INTO issued_books (book_id, borrower_name, due_date) 
    VALUES (p_book_id, p_borrower_name, DATE_ADD(CURDATE(), INTERVAL 14 DAY));
END;
//

DELIMITER ;

CREATE VIEW issued_books_details AS
SELECT ib.issue_id, b.book_id, b.title, b.author, ib.borrower_name, ib.issue_date, ib.due_date
FROM issued_books ib
JOIN books b ON ib.book_id = b.book_id;

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE issued_books;
TRUNCATE TABLE books;
TRUNCATE TABLE users;

SET FOREIGN_KEY_CHECKS = 1;

ALTER TABLE books MODIFY status VARCHAR(50) DEFAULT 'available';

UPDATE books SET status = 'available' WHERE status = 'Available';

DROP PROCEDURE IF EXISTS issue_book;

DELIMITER //

CREATE PROCEDURE issue_book(
    IN p_book_id INT,
    IN p_borrower_name VARCHAR(55)
)
BEGIN
    DECLARE current_status VARCHAR(50);

    SELECT status INTO current_status 
    FROM books 
    WHERE book_id = p_book_id;

    IF current_status = 'issued' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Book already issued';
    ELSE
        INSERT INTO issued_books (book_id, borrower_name, due_date) 
        VALUES (p_book_id, p_borrower_name, DATE_ADD(CURDATE(), INTERVAL 14 DAY));
    END IF;

END //

DELIMITER ;

DROP TRIGGER IF EXISTS after_issue_delete;

DELIMITER //

CREATE TRIGGER after_issue_delete
AFTER DELETE ON issued_books
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM issued_books WHERE book_id = OLD.book_id
    ) THEN
        UPDATE books SET status = 'available' WHERE book_id = OLD.book_id;
    END IF;
END;
//

DELIMITER ;

DELETE FROM issued_books 
WHERE book_id = 6;

SHOW TRIGGERS;

DROP TRIGGER IF EXISTS after_issue_insert;

DELIMITER //

CREATE TRIGGER after_issue_insert
AFTER INSERT ON issued_books
FOR EACH ROW
BEGIN
    UPDATE books 
    SET status = 'issued' 
    WHERE book_id = NEW.book_id;
END;
//

DELIMITER ;

DELETE FROM issued_books 
WHERE book_id IN (2, 3, 6);