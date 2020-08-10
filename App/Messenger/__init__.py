from flask import Blueprint
from App.models import User

bp= Blueprint('messenger', __name__)

try:
	from .routes import *
except Exception as e:
	from routes import *
