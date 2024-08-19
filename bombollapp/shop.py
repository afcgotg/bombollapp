from flask import(
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from .admin import admin_login_required
from .auth import user_login_required
from .db import get_db


bp = Blueprint('shop', __name__, url_prefix='/shop')

@bp.route('/')
def index():
	products = get_products()
	return render_template('shop/index.html', products=products)


def get_products():
	db = get_db()
	products = db.execute(
		'SELECT * FROM product'
	).fetchall()
	return products
	

@bp.route('/view/<int:id>')
def view(id):
	db = get_db()
	product = db.execute(
		'SELECT * FROM product WHERE id = ?',
		(id,)
	).fetchone()
	return render_template('shop/view.html', product=product)

@bp.route('/panel')
def panel():
	products = get_products()	
	return render_template('shop/panel.html', products=products)


def get_product(id):
	db = get_db()
	product = db.execute(
		'SELECT * FROM product WHERE id = ?',
		(id,)
	).fetchone()
	return product


@bp.route('/create', methods=('GET', 'POST'))
@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@admin_login_required
def upsert(id=None):
	product=None
	if id:
		product = get_product(id)

	if request.method == 'POST':
		reference = request.form['reference']
		name = request.form['name']
		description = request.form['description']
		price = request.form['price']
		in_bulk = "in_bulk" in request.form
		stock = request.form['stock']
		
		error = None
		if not reference:
			error = "Producte sense referència."
		if not name:
			error = "Producte sense nom."

		if error is not None:
			flash(error)
		else:
			db = get_db()
			if id:
				db.execute(
					'UPDATE product SET reference = ?, name = ?, '
					'description = ?, price = ?, in_bulk = ?, stock = ? '
					'WHERE id = ?',
					(reference, name, description, price, in_bulk, stock, id)
				)
			else:
				db.execute(
					'INSERT INTO product (reference, name, description, price, '
					'in_bulk, stock) VALUES (?, ?, ?, ?, ?, ?)',
					(reference, name, description, price, in_bulk, stock)
				)
			db.commit()
			return redirect(url_for('shop.panel'))
	
	return render_template('shop/form.html', product=product)


@bp.route('/delete/<int:id>', methods=('POST',))
@admin_login_required
def delete(id):
	db = get_db()
	db.execute(
		'DELETE FROM product WHERE id = ?',
		(id,)
	)
	db.commit()
	return redirect(url_for('shop.panel'))
