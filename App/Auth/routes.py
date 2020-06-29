from App import db
from App.Auth import auth_bp
from flask import render_template, redirect, flash, url_for, request
from App.models import User, Chat
from . import form_validations as fv 

@auth_bp.route('/success', methods= ('GET', ))
def success():
	return "successfull"

@auth_bp.route('/signup', methods= ('GET', 'POST'))
def signup():
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
		
		if errors['username'] is None and errors['email'] is None:
			
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
				return redirect(url_for('auth.success'))

	return render_template('signup.html', title= 'Sign Up', errors= errors, user= user)


@auth_bp.route('/login', methods= ('GET', 'POST'))
def login():
	return render_template('login.html', title= 'Sign Up')
