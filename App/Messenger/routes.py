from App import db, socketio
from App.Messenger import bp
from flask import render_template, redirect, flash, url_for, request, g, jsonify, current_app
from App.models import User, Chat 
from App.Auth.routes import login_required
from flask_socketio import join_room, emit, send, leave_room
from PIL import Image
import os
import secrets
from datetime import datetime
# from App.Auth import form_validations as fv

@bp.route('/index', methods= ('GET', ))
@bp.route('/', methods= ('GET', ))
@login_required
def index():
	current_user= g.user
	friends= current_user.all_friends()
	return render_template('Messenger/index.html', users= friends, current_user= current_user)

@socketio.on('message')
def handle_connect(msg):
	
	emit('acknowledgement', {'status' : 'success'})

@socketio.on('join')
def handle_join(data):
	
	current_user= User.query.filter_by(username = data['name']).first()
	room= current_user.id
	join_room(room)
	send('you are now joined, ' + current_user.username, room= room)

@socketio.on('leave')
def handle_leave(data):
	current_user= User.query.filter_by(username = data['name']).first()
	room= current_user.id
	leave_room(room)
	send('you have left, ' + current_user.username, room= room)

@socketio.on('new message')
def handle_new_message(data):
	
	current_user= User.query.filter_by(username = data['sender']).first()
	name= data['sender']
	data['sender']= current_user.id	
	aux_data= current_user.send_message(message= data['message'], id= data['receiver'])
	if aux_data is False:
		data['success']= False
	else:
		data= aux_data
		data['sender_name']=name
		data['success']= True

	emit('receive message', data, room= data['receiver'])
	emit('new message response', data, room= data['sender'])
# ------------------------------------------------

def save_picture(form_picture, f_ext):
	random_hex = secrets.token_hex(16)
	picture_fn = random_hex + f_ext
	try:
		os.makedirs(os.path.join(current_app.root_path, 'static/images/profile_pictures/'))
	except OSError:
		pass
	picture_path = os.path.join(current_app.root_path, 'static/images/profile_pictures', picture_fn)

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
		profile_pic= request.files['pic_form']
		about= request.form['about_form']

		if profile_pic is not None:
			_, f_ext = os.path.splitext(profile_pic.filename.lower())
			if f_ext in ('.jpg', '.png', '.jpeg'):
				picture_file= save_picture(profile_pic, f_ext)
				current_user.profile_picture= picture_file
		
		if about is not None and about != "":
			current_user.about_me= about
		db.session.commit()
		return redirect(url_for('messenger.explore'))		
	return render_template('Messenger/explore.html', users=users, current_user= current_user)

@socketio.on('send request')
def send_request(data):
	current_user= User.query.filter_by(username = data['sender']).first()
	data['success']= current_user.send_request(data['receiver'])
	data['sender_name']= data['sender']
	data['sender']= current_user.id	
	emit('request received', data, room= data['receiver'])
	emit('send request response', data, room= data['sender'])

@socketio.on('accept request')
def accept_request(data):
	current_user= User.query.filter_by(username = data['sender']).first()
	data['success']= current_user.accept_request(data['receiver'])
	data['sender_name']= data['sender']
	data['sender']= current_user.id
	emit('request accepted', data, room= data['receiver'])
	emit('accept request response', data, room= data['sender'])

@socketio.on('delete request')
def delete_request(data):
	current_user= User.query.filter_by(username = data['sender']).first()
	data['success']= current_user.unfriend(data['receiver'])
	data['sender_name']= data['sender']
	data['sender']= current_user.id
	emit('request deleted', data, room= data['receiver'])
	emit('delete request response', data, room= data['sender'])
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
	response['chat']= messages
	response['last_message']= current_user.get_last_message(id)
	return jsonify(response)

	