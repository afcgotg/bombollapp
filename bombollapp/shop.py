from flask import(
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from .admin import admin_login_required
from .auth import user_login_required
from .db import get_db


bp = Blueprint('shop', __name__, url_prefix='/shop')

@bp.route('/')
def index():
	db = get_db()
	products = db.execute(
		'SELECT * FROM product'
	).fetchall()
	return render_template('shop/index.html', products=products)


@bp.route('/view/<string:reference>')
def view(reference):
	db = get_db()
	product = db.execute(
		'SELECT * FROM product WHERE reference = ?',
		(reference,)
	).fetchone()
	return render_template('shop/view.html', product=product)

