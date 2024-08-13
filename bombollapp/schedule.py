from flask import(
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from .admin import admin_login_required
from .auth import user_login_required
from .db import get_db


bp = Blueprint('schedule', __name__, url_prefix='/schedule')


@bp.route('/')
def index():
	db = get_db()
	events = db.execute(
		'SELECT e.id, title, description, date, size FROM event e ORDER BY date DESC'
	).fetchall()
	return render_template('schedule/index.html', events=events)


@bp.route('/create', methods=('GET', 'POST'))
@admin_login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		description = request.form['description']
		date = request.form['date']
		size = request.form['size']
		error = None

		if not title:
			error = "Títol requerit."
		elif not description:
			error = "Descripció requerida."
		elif not date:
			error = "Data requerida."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO event (title, description, date, size) VALUES'
				' (?, ?, ?, ?)',
				(title, description, date, size)
			)
			db.commit()
			return redirect(url_for('schedule.index'))
	return render_template('schedule/create.html')


def get_event(id):
	event = get_db().execute(
		'SELECT e.id, title, description, date, size FROM event e'
		' WHERE e.id = ?',
		(id,)
	).fetchone()

	if event is None:
		abort(404, f"L'event amb id {id} no existeix.")

	return event


@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@admin_login_required
def update(id):
	event = get_event(id)

	if request.method == 'POST':
		title = request.form['title']
		description = request.form['description']
		date = request.form['date']
		size = request.form['size']

		error = None
		
		if not title:
			error = "Títol requerit."
		elif not description:
			error = "Descripció requerida."
		elif not date:
			error = "Data requerida."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE event SET title = ?, description = ?, date = ?,'
				' size = ? WHERE id = ?',
				(title, description, date, size, id)
			)
			db.commit()
			return redirect(url_for('schedule.index'))

	return render_template('schedule/update.html', event=event)


@bp.route('/delete/<int:id>', methods=('POST',))
@admin_login_required
def delete(id):
	get_event(id)
	db = get_db()
	db.execute('DELETE FROM event_user WHERE event_id = ?', (id,))
	db.execute('DELETE FROM event WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('schedule.index'))


@bp.route('/adduser/<int:event_id>/<int:user_id>', methods=('POST',))
@user_login_required
def adduser(event_id, user_id):
	db.get_db().execute(
		'INSERT INTO event_user (event_id, user_id) VALUES (?, ?)',
		(event_id, user_id)
	)
	db.commit()
	return redirect(url_for('schedule.index'))


@bp.route('/removeuser/<int:event_id>/<int:user_id>', methods=('POST',))
@user_login_required
def removeuser(event_id, user_id):
	db.get_db().execute(
		'DELETE FROM event_user WHERE (event_id, user_id) = (?, ?)',
		(event_id, user_id)
	)
	db.commit()
	return redirect(url_for('schedule.index'))
