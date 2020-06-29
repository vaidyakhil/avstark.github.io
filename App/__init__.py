from flask import Flask
from .config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db= SQLAlchemy()
migrate= Migrate()

def create_app(config_class= Config):
	app= Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)

	with app.app_context():
		db.create_all()

	from App.Auth import auth_bp
	app.register_blueprint(auth_bp, url_prefix= '/auth')

	return app