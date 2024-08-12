from flask import(
	Blueprint, g, render_template, request, session, url_for
)

from .db import get_db


bp = Blueprint('about', __name__, '/about')

@bp.route('/')
def about():
	db = get_db()
	info = db.execute('SELECT * FROM about').fetchone()
	return render_template('about.html')
