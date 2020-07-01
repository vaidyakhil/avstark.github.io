from flask import Blueprint
from App.models import User

bp= Blueprint('messenger', __name__, template_folder= 'templates')

from .routes import *
