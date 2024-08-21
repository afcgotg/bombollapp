import sqlite3

import click
from flask import current_app, g
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
	if 'db' not in g:
		g.db = sqlite3.connect(
			current_app.config['DATABASE'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db.row_factory = sqlite3.Row

	return g.db


def close_db(e=None):
	db = g.pop('db', None)
	if db is not None:
		db.close()


def init_db():
	db = get_db()

	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))

	db.execute(
		'INSERT INTO about (description, phone, addres) values '
		'("Descripció de la botiga.", "", "")'
	)
	db.commit()


@click.command('init-db')
def init_db_command():
	init_db()
	click.echo("Database initialized.")

@click.command('create-admin')
@click.argument('username')
@click.argument('password')
def create_admin_command(username, password):
	db = get_db()
	try:
		db.execute(
			'INSERT INTO admin (username, password) values (?, ?)',
			(username, generate_password_hash(password)),
		)
		db.commit()
	except db.IntegrityError:
		print(f"{username} already exists.")
	else:
		print("Admin created.")


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(create_admin_command)
