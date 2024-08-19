from flask import(
	Blueprint, g, render_template, request, session, url_for, redirect
)

from .db import get_db


bp = Blueprint('about', __name__, url_prefix='/about')

def get_about_info(id=1):
	db = get_db()
	info = db.execute(
		'SELECT * FROM about WHERE id = ?',
		(id,)
	).fetchone()
	return info
	

@bp.route('/')
def about():
	info = get_about_info()
	return render_template('about/about.html', info=info)


@bp.route('/update', methods=('GET', 'POST'))
def update():
	info = get_about_info()

	if request.method == 'POST':
		description = request.form['description']
		phone = request.form['phone']
		addres = request.form['addres']

		db = get_db()
		db.execute(
			'UPDATE about SET description = ?, phone = ?, addres = ?'
			' WHERE id = ?',
			(description, phone, addres, info['id'])
		)
		db.commit()
		return redirect(url_for('about.about'))

	return render_template('about/form.html', info=info)




