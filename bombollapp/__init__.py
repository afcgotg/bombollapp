import os

from flask import Flask, render_template

from . import db, auth, admin, about, blog


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE=os.path.join(app.instance_path, 'bombollapp.sqlite'),
	)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/')
	def home():
		return render_template('base_layout.html')

	db.init_app(app)

	app.register_blueprint(auth.bp)
	app.register_blueprint(admin.bp)
	app.register_blueprint(about.bp)
	app.register_blueprint(blog.bp)

	return app
