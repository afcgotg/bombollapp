import functools

from flask import(
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		password = request.form['password']

		phone = request.form['phone']
		addres = request.form['addres']
		
		db = get_db()
		error = None

		if not email:
			error = "Es requereix un correu electrònic."
		elif not password:
			error = "Es requereix una contrassenya."

		if error is None:
			try:
				db.execute(
					"""INSERT INTO user (
						email, password, first_name, last_name, phone, addres
					) values (?, ?, ?, ?, ?, ?)""",
					(email, generate_password_hash(password), first_name,
					last_name, phone, addres),
				)
				db.commit()
			except db.IntegrityError:
				error = f"Aquest email ja està registrat."
			else:
				return redirect(url_for('auth.login'))

		flash(error)

	return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']

		db = get_db()
		error = None

		user = db.execute(
			'SELECT * FROM user WHERE email = ?', (email,)
		).fetchone()

		if user is None:
			error = "Email no registrat."
		elif not check_password_hash(user['password'], password):
			error = "Contrasenya incorrecte."

		if error is None:
			session.clear()
			session['user_id'] = user['id']
			return redirect(url_for('home'))

		flash(error)

	return render_template('/auth/login.html')


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = get_db().execute(
			'SELECT * FROM user WHERE id = ?', (user_id, )
		).fetchone()


@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))


def user_login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)

	return wrapped_view


