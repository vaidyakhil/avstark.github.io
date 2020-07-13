from App import db
from App.Auth import auth_bp 
from flask import render_template, redirect, flash, url_for, request, session, g
from App.models import User, Chat
from App.Auth import form_validations as fv 
import functools
from App.Auth.email import password_reset_email, verify_user_email
from datetime import datetime

@auth_bp.route('/reset_password/<token>', methods= ('GET', 'POST'))
def reset_password(token):
	if g.user:
		flash("You are already logged in!")
		return redirect(url_for('messenger.index'))

	id= User.verify_token(token)
	if id is None:
		flash("Either the reset password mail expired or something else went down. Please try again")
		return redirect(url_for('auth.reset_password_request'))
	
	new_password= ""
	error= None
	if request.method == 'POST':
		user= User.query.filter_by(id = id).first()
		new_password= request.form['new_password']
		error= fv.data_required(new_password, "password")
		if error is None:
			user.set_password(new_password)
			db.session.commit()
			flash("Your password has been successfully reset.")
			return redirect(url_for('auth.login'))

	return render_template('Auth/reset_password.html', error= error, new_password= new_password)

@auth_bp.route('/reset_password_request', methods= ('GET', 'POST'))
def reset_password_request():
	if g.user:
		flash("You are already logged in!")
		return redirect(url_for('messenger.index'))

	error= None
	credential= ""
	if request.method == 'POST':
		credential= request.form['credential']
		
		error= fv.data_required(credential)
		if error is None:
			flash("A recovery email is sent to you with further instructions.")
			user= User.query.filter_by(email = credential).first()
			if user is None:
				user= User.query.filter_by(username = credential).first()
			if user is not None:
				password_reset_email(user)
			return redirect(url_for('auth.login'))

	return render_template('Auth/reset_password_request.html', title= 'Sign Up', error= error, credential= credential)

@auth_bp.route('/signup', methods= ('GET', 'POST'))
def signup():
	if g.user:
		flash("You are already logged in!")
		return redirect(url_for('messenger.index'))

	errors= {}
	user={}

	if request.method == 'POST':
		user['username']= request.form['username']
		user['email']= request.form['email']
		password= request.form['password']
		try:
			user['gender']= request.form['gender']
			print(user['gender'])
		except Exception as e:
			errors['gender']= "This field is required"

		user['about']= request.form['about']

		errors['username']= fv.data_required(user['username'], 'username')
		errors['email']= fv.validate_email(user['email'], 'email')
		errors['password']= fv.data_required(password, 'password')
		if errors['username'] is None and errors['email'] is None and errors['password'] is None:
			
			u= User.query.filter(User.username == user['username']).first()
			if u is not None:
				errors['username']= "Please choose a different username"
			
			u= User.query.filter(User.email == user['email']).first()
			if u is not None:
				errors['email']= "Incorrect Email Address"
			
			if errors['username'] is None and errors['email'] is None:
				user= User(username= user['username'], 
					email= user['email'], 
					password= password, 
					gender= user['gender'], 
					about_me= user['about'])
				db.session.add(user)
				db.session.commit()
				# verify_user_email(user)
				# flash("An Authentication mail has been sent to you. Please follow the instructions.")
				# in production uncomment these lines of code
				return redirect(url_for('auth.login'))

	return render_template('Auth/signup.html', title= 'Sign Up', errors= errors, user= user)

@auth_bp.route('/verify_user<token>')
def verify_user(token):
	if g.user:
		flash("You are already logged in!")
		return redirect(url_for('messenger.index'))

	id= User.verify_token(token)
	if id is None:
		flash("something went wrong. Please try again")
		return redirect(url_for('auth.signup'))

	user= User.query.filter_by(id = id).first()
	user.verified= True
	db.session.commit()
	flash("You have been autheticated successfully. Welcome to chatbox.")
	return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods= ('GET', 'POST'))
def login():
	if g.user:
		flash("You are already logged in!")
		return redirect(url_for('messenger.index'))

	errors={}
	if request.method == 'POST':
		username= request.form['username']
		password=request.form['password']
		errors['username']= fv.data_required(username, 'username')
		errors['password']= fv.data_required(password, 'password')
		
		if errors["username"] is None and errors["password"] is None:
			u= User.query.filter(User.username == username).first()
			if u is not None:
				check= u.check_password(password)
				if check:
					if u.verified:
						session.clear()
						session['user_id']= u.id
						return redirect(url_for('messenger.index'))
					else:
						flash("Authentication Incomplete! Please follow the instructions in your signup email.")
						return redirect(url_for('auth.login'))

			flash("Invalid Credentials")		

	return render_template('Auth/login.html', title= 'Login', errors= errors)

@auth_bp.route('/logout')
def logout():
	session.clear()
	# g.user= None	
	return redirect(url_for('auth.login'))

@auth_bp.before_app_request
def load_user():
	user_id= session.get('user_id')
	if user_id is None:
		g.user= None
	else:
		g.user= User.query.filter(User.id == user_id).first()
		g.user.last_seen= datetime.utcnow()
		db.session.commit()

def login_required(view):
	@functools.wraps(view)
	def wrapper_func(**kwargs):
		if g.user is None:
			flash("Too Bad, if only you could login!")
			return redirect(url_for('auth.login'))
		return view(**kwargs)

	return wrapper_func