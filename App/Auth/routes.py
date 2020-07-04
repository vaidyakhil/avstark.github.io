from App import db
from App.Auth import auth_bp
from flask import render_template, redirect, flash, url_for, request, session, g
from App.models import User, Chat
from . import form_validations as fv 
import functools

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
		except Exception as e:
			errors['gender']= "This field is required"

		user['about']= request.form['about']

		errors['username']= fv.data_required(user['username'], 'username')
		errors['email']= fv.validate_email(user['email'], 'email')
		errors['password']= fv.data_required(password, password)
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
				return redirect(url_for('auth.login'))

	return render_template('Auth/signup.html', title= 'Sign Up', errors= errors, user= user)


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
		
		if username is not None and password is not None:
			u= User.query.filter(User.username == username).first()
			if u is not None:
				check= u.check_password(password)
				if check:
					session.clear()
					session['user_id']= u.id
					return redirect(url_for('messenger.index'))

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

def login_required(view):
	@functools.wraps(view)
	def wrapper_func(**kwargs):
		if g.user is None:
			flash("Too Bad, if only you could login!")
			return redirect(url_for('auth.login'))
		return view(**kwargs)

	return wrapper_func