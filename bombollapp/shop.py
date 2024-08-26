import os

from flask import(
	Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.utils import secure_filename

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

def get_product_from_form():
	product = {}
	product['reference'] = request.form['reference']
	product['name'] = request.form['name']
	product['description'] = request.form['description']
	product['price'] = request.form['price']
	product['in_bulk'] = "in_bulk" in request.form
	product['stock'] = request.form['stock']
	
	error = validate_data(product)

	return (product, error)
	
def validate_data(product):
	error = None
	if not product['reference']:
		error = "Producte sense referència."
	if not product['name']:
		error = "Producte sense nom."
	if product['price']:
		try:
			product['price'] = float(product['price'])
		except ValueError:
			error = "El preu ha de ser un valor numèric."
	if product['stock']:
		try:
			product['stock'] = int(product['stock'])
		except ValueError:
			error = "L'stock ha de ser un nombre enter."
		else:
			if product['stock'] < 0:
				error = "L'stock ha de ser un nombre positiu."	
	return error

def query_format(product, id=None):
	product_tuple = (product['reference'], product['name'],
		product['description'], product['price'], product['in_bulk'],
		product['stock'])
	if id:
		product_tuple = product_tuple + (id,)
	return product_tuple

@bp.route('/create', methods=('GET', 'POST'))
@admin_login_required
def create():
	product=None
	if request.method == 'POST':
		product, error = get_product_from_form()
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'INSERT INTO product (reference, name, description, price, '
				'in_bulk, stock) VALUES (?, ?, ?, ?, ?, ?)',
				query_format(product)
			)
			db.commit()
			return redirect(url_for('shop.panel'))
	
	return render_template('shop/form.html', product=product)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@admin_login_required
def update(id=None):
	product = get_product(id)
	if request.method == 'POST':
		product, error = get_product_from_form()
		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE product SET reference = ?, name = ?, '
				'description = ?, price = ?, in_bulk = ?, stock = ? '
				'WHERE id = ?',
				query_format(product, id)
			)
			db.commit()
			files = request.files.getlist('images')
			for file in files:
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					folder = os.getcwd() + '/bombollapp/static/img/shop/' + str(id)
					os.makedirs(folder, exist_ok=True)
					file.save(os.path.join(folder, filename))
			return redirect(url_for('shop.panel'))
	
	return render_template('shop/form.html', product=product, id=id)


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
