from flask import(
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from .admin import admin_login_required
from .auth import user_login_required
from .db import get_db


bp = Blueprint('agenda', __name__, url_prefix='/agenda')


@bp.route('/')
def index():
	db = get_db()
	events = db.execute(
		'SELECT e.id, title, summary, description, date, size, current '
		'FROM event e ORDER BY date ASC'
	).fetchall()
	events_user = get_events_user()
	return render_template('agenda/index.html',
		events=events,
		events_user=events_user
	)

@bp.route('/create', methods=('GET', 'POST'))
@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@admin_login_required
def update(id=None):
	event = None
	if id:
		event = get_event(id)
	
	if request.method == 'POST':
		title = request.form['title']
		summary = request.form['summary']
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
			if not id:
				db.execute(
					'INSERT INTO event (title, summary, description, date, '
					'size) VALUES'
					' (?, ?, ?, ?, ?)',
					(title, summary, description, date, size)
				)
			else:
				db.execute(
					'UPDATE event SET title = ?, summary= ?, description = ?, '
					'date = ?, size = ? WHERE id = ?',
					(title, summary, description, date, size, id)
				)
			db.commit()
			return redirect(url_for('agenda.index'))

	return render_template('agenda/form.html', event=event)


@bp.route('/delete/<int:id>', methods=('POST',))
@admin_login_required
def delete(id):
	get_event(id)
	db = get_db()
	db.execute('PRAGMA foreign_keys = ON')
	db.execute('DELETE FROM event WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('agenda.index'))


@bp.route('/adduser/<int:event_id>', methods=('POST',))
@user_login_required
def adduser(event_id):
	db = get_db()
	try:
		db.execute(
			'INSERT INTO event_user (event_id, user_id) VALUES (?, ?)',
			(event_id, g.user['id'])
		)
		db.execute(
			'UPDATE event SET current = current + 1 WHERE id = ?',
			(event_id,)
		)
		db.commit()

	except db.IntegrityError:
		pass

	return redirect(request.referrer)


@bp.route('/removeuser/<int:event_id>', methods=('POST',))
@user_login_required
def removeuser(event_id):
	db = get_db()
	db.execute(
		'DELETE FROM event_user WHERE (event_id, user_id) = (?, ?)',
		(event_id, g.user['id'])
	)
	db.execute(
		'UPDATE event SET current = current - 1 WHERE id = ?',
		(event_id,)
	)
	db.commit()
	return redirect(request.referrer)


@bp.route('/view/<int:event_id>', methods=('GET',))
def view(event_id):
	db = get_db()
	event = session.get('event')
	users_event = db.execute(
		'SELECT u.first_name, u.last_name FROM event_user eu'
		' INNER JOIN user u ON u.id = eu.user_id'
		' WHERE eu.event_id = ?',
		(event_id,)
	).fetchall()
	db.commit()
	events_user = get_events_user()

	return 	render_template('agenda/view.html', event=event,
		users_event=users_event, events_user=events_user)


def get_event(id):
	event = get_db().execute(
		'SELECT e.id, title, summary, description, date, size, current FROM event e'
		' WHERE e.id = ?',
		(id,)
	).fetchone()

	if event is None:
		abort(404, f"L'event amb id {id} no existeix.")

	return event


def get_events_user():
	events_user = None
	if g.user:
		db = get_db()
		events_user = db.execute(
        	'SELECT eu.event_id FROM event_user eu WHERE eu.user_id = ?',
        	(g.user['id'],)
	    ).fetchall()
		events_user = [e['event_id'] for e in events_user]

	return events_user
