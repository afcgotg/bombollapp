import functools
from flask import(
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		db = get_db()
		error = None

		admin = db.execute(
			'SELECT * FROM admin WHERE username = ?', (username,)
		).fetchone()

		if admin is None:
			error = "Nom d'usuari incorrecte."
		elif not check_password_hash(admin['password'], password):
			error = "Contrasenya incorrecte."

		if error is None:
			session.clear()
			session['admin_id'] = admin['id']
			return redirect(url_for('home'))

		flash(error)

	return render_template('/admin/login.html')


@bp.before_app_request
def load_logged_in_admin():
	admin_id = session.get('admin_id')

	if admin_id == None:
		g.admin = None
	else:
		g.admin = get_db().execute(
			'SELECT * FROM admin WHERE id = ?', (admin_id, )
		).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))

def admin_login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.admin is None:
			return redirect(url_for('admin.login'))

		return view(**kwargs)

	return wrapped_view
