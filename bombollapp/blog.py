from flask import(
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .admin import admin_login_required
from .db import get_db


bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
def index():
	db = get_db()
	posts = db.execute(
		'SELECT p.id, title, body, created FROM post p ORDER BY created DESC'
	).fetchall()
	return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@admin_login_required
def create():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = "Títol requerit."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO post (title, body) VALUES (?, ?)',
				(title, body)
			)
			db.commit()
			return redirect(url_for('blog.index'))

	return render_template('blog/create.html')


def get_post(id):
	post = get_db().execute(
		'SELECT p.id, title, body, created FROM post p WHERE p.id = ?',
		(id,)
	).fetchone()

	if post is None:
		abort(404, f"El post amb id {id} no existeix.")

	return post

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@admin_login_required
def update(id):
	post = get_post(id)

	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		error = None

		if not title:
			error = "Títol requerit."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE post SET title = ?, body = ?'
				' WHERE id = ?',
				(title, body, id)
			)
			db.commit()
			return redirect(url_for('blog.index'))

	return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:id>', methods=('POST',))
@admin_login_required
def delete(id):
	get_post(id)
	db = get_db()
	db.execute('DELETE FROM post WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('blog.index'))
