from App import db, socketio
from App.Messenger import bp
from flask import render_template, redirect, flash, url_for, request, g, jsonify, current_app
from App.models import User, Chat 
from App.Auth.routes import login_required
from flask_socketio import join_room, emit, send
from PIL import Image
import os
import secrets
# from App.Auth import form_validations as fv

@bp.route('/index', methods= ('GET', ))
@bp.route('/', methods= ('GET', ))
@login_required
def index():
	current_user= g.user
	friends= current_user.all_friends()
	return render_template('Messenger/index.html', users= friends, current_user= current_user)

def save_picture(form_picture, f_ext):
	random_hex = secrets.token_hex(16)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(current_app.root_path, 'static/images', picture_fn)

	output_size = (200, 200)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@bp.route('/explore', methods= ('GET', 'POST'))
@login_required
def explore():
	current_user= g.user
	users= User.query.all()
	users.remove(current_user)

	if request.method == 'POST':
		print(request.form)
		profile_pic= request.files['pic_form']
		about= request.form['about_form']

		if profile_pic is not None:
			_, f_ext = os.path.splitext(profile_pic.filename)
			if f_ext in ('.jpg', '.png', '.jpeg'):
				picture_file= save_picture(profile_pic, f_ext)
				current_user.profile_picture= picture_file
				print(current_user.profile_picture)
		
		if about is not None and about != "":
			current_user.about_me= about
		db.session.commit()
		return redirect(url_for('messenger.explore'))		
	return render_template('Messenger/explore.html', users=users, current_user= current_user)

# ------------------------------------------------

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

#------------------------------------------

@bp.route('/get_chat/id=<int:id>')
@login_required
def get_chat(id):
	current_user= g.user
	response= {}
	messages= current_user.get_chat(id)
	if messages == False:
		response['success']= False
		flash("Something unexpected has occured. Please refresh the page")
		return jsonify(response)

	response['success']= True
	response['chat']= render_template('Messenger/chat.html', messages= messages, current_user= current_user, userid= id)
	response['last_message']= current_user.get_last_message(id)
	return jsonify(response)

@bp.route('/send_message', methods= ('POST',))
@login_required
def send_message():
	current_user= g.user
	id= request.form['id']
	message= request.form['message']
	success= current_user.send_message(message= message, id= id)
	print(message, id)
	# messages= current_user.get_chat(id)
	# response['success']= True
	# response['data']= render_template('Messenger/chat.html', messages= messages, current_user= current_user, userid= id)
	return jsonify(success)
		

# @socketio.on('sent_message')
# def sent_message(data):
	