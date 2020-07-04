from flask import Blueprint
from App.models import User

bp= Blueprint('messenger', __name__)

from .routes import *
