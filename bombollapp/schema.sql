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


DROP TABLE IF EXISTS post;
CREATE TABLE post(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	body TEXT NOT NULL,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);


DROP TABLE IF EXISTS event;
CREATE TABLE event(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT NOT NULL,
	summary TEXT NOT NULL,
	description TEXT NOT NULL,
	date DATETIME NOT NULL,
	size INTEGER,
	current INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS event_user;
CREATE TABLE event_user(
	event_id INTEGER,
	user_id INTEGER,
	FOREIGN KEY (event_id) REFERENCES event (id) ON DELETE CASCADE,
	FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE CASCADE
);


DROP TABLE IF EXISTS product;
CREATE TABLE product(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	reference TEXT UNIQUE NOT NULL,
	name TEXT NOT NULL,
	description TEXT,
	price FLOAT,
	in_bulk BOOLEAN DEFAULT 0,
	stock INTEGER DEFAULT 0
);

DROP TABLE IF EXISTS label;
CREATE TABLE label(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL
);

DROP TABLE IF EXISTS product_label;
CREATE TABLE product_label(
	product_id INTEGER,
	label_id INTEGER,
	FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE,
	FOREIGN KEY (label_id) REFERENCES label(id) ON DELETE CASCADE
);
