from App import db
from App.Messenger import bp
from flask import render_template, redirect, flash, url_for, request
from App.models import User, Chat 
from App.Auth.routes import login_required

@bp.route('/index', methods= ('GET', ))
@bp.route('/', methods= ('GET', ))
@login_required
def index():
	return render_template('Messenger/index.html')

@bp.route('/explore', methods= ('GET', 'POST'))
@login_required
def explore():
	users= User.query.all()
	return render_template('Messenger/explore.html', users=users)
