from App.Auth import auth_bp
from flask import render_template, redirect, flash, url_for

@auth_bp.route('/signup', methods= ('GET', 'POST'))
def signup():
	return render_template('signup.html', title= 'Sign Up')

@auth_bp.route('/login', methods= ('GET', 'POST'))
def login():
	return render_template('login.html', title= 'Sign Up')
