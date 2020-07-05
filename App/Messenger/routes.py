from App import db
from App.Messenger import bp
from flask import render_template, redirect, flash, url_for, request,g 
from App.models import User, Chat 
from App.Auth.routes import login_required

@bp.route('/index', methods= ('GET', ))
@bp.route('/', methods= ('GET', ))
@login_required
def index():
	current_user= g.user
	friends= current_user.all_friends()
	return render_template('Messenger/index.html', friends= friends, current_user= current_user)

@bp.route('/explore', methods= ('GET', 'POST'))
@login_required
def explore():
	current_user= g.user
	users= User.query.all()
	users.remove(current_user)
	return render_template('Messenger/explore.html', users=users, current_user= current_user)
