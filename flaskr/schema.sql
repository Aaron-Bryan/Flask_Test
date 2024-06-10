--Time to learn sql lmao

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    );

CREATE TABLE post (
    id INTEGER,
    author_id INTEGER,
    created TIMESTAMP,
    post_title TEXT,
    post_body TEXT
    );