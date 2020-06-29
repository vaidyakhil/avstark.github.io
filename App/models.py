from App import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
	"""id, name, email-address, password_hash, about_me"""

	__tablename__= 'user'
	
	id= db.Column(db.Integer, primary_key= True, nullable= False)

	username= db.Column(db.String(32), unique= True, nullable= False, index= True)

	email= db.Column(db.String(80), unique= True, nullable= False, index= True)

	password_hash= db.Column(db.String(256))

	about_me= db.Column(db.String(128))

	sent= db.relationship('Chat', backref= 'author', foreign_keys= 'Chat.sender', lazy= 'dynamic')

	received= db.relationship('Chat', backref= 'recipient', foreign_keys= 'Chat.receiver', lazy= 'dynamic')

	def set_password(self, password):
		self.password_hash= generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __init__(self, username, email, password, about_me= None,  *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		self.username= 	username
		self.email=	email
		self.set_password(password)
		self.about_me= about_me

	def __repr__(self):
		return 'User object: id {} username {}'.format(self.id, self.username)

class Chat(db.Model):
	__tablename__=  "chat"

	id= db.Column(db.Integer, primary_key= True, nullable= False)

	message= db.Column(db.String(), nullable= False)

	sender= db.Column(db.Integer, db.ForeignKey('user.id'))

	receiver= db.Column(db.Integer, db.ForeignKey('user.id'))

	timestamp= db.Column(db.DateTime, index= True, default= datetime.utcnow)

	def __init__(self, message, sender_id, receiver_id, timestamp= datetime.utcnow, *args, **kwargs):
		self.message= message
		self.sender_id= sender_id
		self.receiver_id= receiver_id	

	def __repr__(self):
		return 'Chat object: sender_id {} and receiver_id {}'.format(self.sender_id, self.receiver_id)
