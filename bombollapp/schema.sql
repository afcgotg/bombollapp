DROP TABLE IF EXISTS user;
CREATE TABLE user(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email TEXT UNIQUE NOT NULL,
	password TEXT NOT NULL,
	first_name TEXT NOT NULL,
	last_name TEXT NOT NULL,
	phone TEXT,
	addres TEXT
);


DROP TABLE IF EXISTS admin;
CREATE TABLE admin(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username TEXT UNIQUE NOT NULL,
	password TEXT UNIQUE NOT NULL
);


DROP TABLE IF EXISTS about;
CREATE TABLE about(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	description TEXT,
	phone TEXT,
	addres TEXT
);
INSERT INTO about (description, phone, addres) values ("", "", "");

DROP TABLE IF EXISTS post;
CREATE TABLE post(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	body TEXT NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
