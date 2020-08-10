from flask import Blueprint

auth_bp= Blueprint('auth', __name__)

try:
	from .routes import *
except Exception as e:
	from App.Auth.routes import *
