from App import mail
from flask_mail import Message
from threading import Thread
from flask import current_app

def send_asnc_email(app, msg):
	with app.app_context():
		mail.send(msg)

def send_email(subject, sender, recipients, textbody, htmlbody):
	msg= Message(subject, sender= sender, recipients=recipients)
	msg.body= textbody
	msg.html= htmlbody
	Thread(target= send_asnc_email, args= (current_app._get_current_object(), msg)).start()