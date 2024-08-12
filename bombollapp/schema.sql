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
	description TEXT,
	phone TEXT,
	addres TEX
);
INSERT INTO about (description, phone, addres) values ("", "", "")

