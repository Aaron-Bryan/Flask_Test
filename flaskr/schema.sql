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

CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    post_title TEXT NOT NULL,
    post_body TEXT NOT NULL,
    FOREIGN KEY(author_id) REFERENCES user(id)
    );