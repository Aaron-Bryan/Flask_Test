--Time to learn sql lmao

--Removes the following tables if they exist
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

--Creates a Table called user
CREATE TABLE user (
    --Primary key is id and is also automatically generated
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    --username must be unique and not null
    username TEXT UNIQUE NOT NULL,
    --password must not be null
    password TEXT NOT NULL
    );

--Creates a Table called post
CREATE TABLE post (
    --Primary key is id and is also automatically generated
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    --author_id must be integer and not null
    author_id INTEGER NOT NULL,
    --created is a date/time value
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    --post_title is a text value that must not be null
    post_title TEXT NOT NULL,
    --post_title is a text value that must not be null
    post_body TEXT NOT NULL,
    --sets the author_id as a foreign key that references the id column from the user table
    FOREIGN KEY(author_id) REFERENCES user(id)
    );