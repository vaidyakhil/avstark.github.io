from App.email import send_email
from flask import render_template, current_app

def password_reset_email(user):
	token= user.get_token()
	
	recipients= [user.email]
	subject= "re: [chatbox] Reset Password"
	sender= current_app.config['ADMINS'][0]
	textbody= render_template("Auth/email_reset_password_text.txt", user= user, token= token)
	htmlbody= render_template("Auth/email_reset_password_html.html", user= user, token= token)

	send_email(subject= subject, sender= sender, recipients= recipients, textbody= textbody, htmlbody= htmlbody)

def verify_user_email(user):
	token= user.get_token()
	
	recipients= [user.email]
	subject= "re: [chatbox] Verify New User"
	sender= current_app.config['ADMINS'][0]
	textbody= render_template("Auth/email_verify_user_text.txt", user= user, token= token)
	htmlbody= render_template("Auth/email_verify_user_html.html", user= user, token= token)

	send_email(subject= subject, sender= sender, recipients= recipients, textbody= textbody, htmlbody= htmlbody)