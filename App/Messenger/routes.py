from App import db
from App.Messenger import bp
from flask import render_template, redirect, flash, url_for, request,g, jsonify 
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

@bp.route('/send_request/id=<int:id>')
@login_required
def send_request(id):
	current_user= g.user
	success= current_user.send_request(id)
	return jsonify({'success' : success})

@bp.route('/delete_request/id=<int:id>')
@login_required
def delete_request(id):
	current_user= g.user
	success= current_user.unfriend(id)
	return jsonify({'success' : success})

@bp.route('/accept_request/id=<int:id>')
@login_required
def accept_request(id):
	current_user= g.user
	success= current_user.accept_request(id)
	return jsonify({'success' : success})