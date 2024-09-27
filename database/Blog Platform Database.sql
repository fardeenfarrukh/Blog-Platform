create database blog_platform;
use blog_platform;
drop table users;
drop table posts;
drop table comments;
drop table tags;
drop table posts_tags;
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('Admin', 'Author', 'Reader') NOT NULL DEFAULT 'Reader',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE posts (
    post_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(100),
    tags TEXT
);
CREATE TABLE comments (
    comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER REFERENCES posts(post_id),
    user_id INTEGER REFERENCES users(user_id),
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE tags (
    tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE post_tags (
    post_tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER REFERENCES posts(post_id),
    tag_id INTEGER REFERENCES tags(tag_id)
);

insert into users(username, password_hash, email, role)
values
('admin', 'hashed_admin_password', 'admin@gmail.com', 'Admin'),
('author1', 'hashed_author_password', 'author1@gmail.com', 'Author'),
('reader1', 'hashed_reader_password', 'reader1@gmail.com', 'Reader');
insert into posts(title, content, author_id, category, tags)
values
('First Blog Update', 'Greetings everyone to our blog!', 2, 'General', 'greetings,first post');
insert into comments(post_id, user_id, comment)
values
(1, 3, 'First Post! Hope everyone like it and expect more in the future.');
insert into tags(tag_name)
values
('Greetings'),
('first post');
insert into post_tags(post_id, tag_id)
values
(1, 1),
(1, 2);