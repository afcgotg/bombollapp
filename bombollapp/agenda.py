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

def get_event_from_form():
	event = {}
	event['title'] = request.form['title']
	event['summary'] = request.form['summary']
	event['description'] = request.form['description']
	event['date'] = request.form['date']
	event['size'] = request.form['size']

	error = validate_data(event)
	return (event, error)
	
def validate_data(event):
	error = None
	if not event['title']:
		error = "Títol requerit."
	elif not event['description']:
		error = "Descripció requerida."
	elif not event['date']:
		error = "Data requerida."
	elif not event['size']:
		event['size'] = 0
	try:	
		event['size'] = int(event['size'])
	except ValueError:
		error = "El nombre de places ha de ser un valor enter."
	else:
		if event['size'] < 0:
			error = "El nombre de places ha de ser un valor positiu."

	print(event['size'])
	return error

def query_format(event, id=None):
	event_tuple = (event['title'], event['summary'], event['description'],
		event['date'], event['size'])
	if id:
		event_tuple = event_tuple + (id,)

	return event_tuple
		

@bp.route('/create', methods=('GET', 'POST'))
@admin_login_required
def create():
	event = None
	if request.method == 'POST':
		event, error = get_event_from_form()
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO event (title, summary, description, date, '
				'size) VALUES'
				' (?, ?, ?, ?, ?)',
				query_format(event),
			)
			db.commit()
			return redirect(url_for('agenda.index'))

	return render_template('agenda/form.html', event=event)

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@admin_login_required
def update(id=None):
	event = get_event(id)
	
	if request.method == 'POST':
		event, error = get_event_from_form()
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE event SET title = ?, summary= ?, description = ?, '
				'date = ?, size = ? WHERE id = ?',
				query_format(event, id)
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


@bp.route('/view/<int:id>', methods=('GET',))
def view(id):
	event = get_event(id)
	db = get_db()
	users_event = db.execute(
		'SELECT u.first_name, u.last_name FROM event_user eu'
		' INNER JOIN user u ON u.id = eu.user_id'
		' WHERE eu.event_id = ?',
		(id,)
	).fetchall()
	db.commit()
	events_user = get_events_user()

	return 	render_template('agenda/view.html', event=event,
		users_event=users_event, events_user=events_user, id=id)


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
