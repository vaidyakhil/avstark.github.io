from App import create_app, db, socketio
from App.models import Chat, User, Friendship

app= create_app()
@app.shell_context_processor
# this is for the flask shell so that on starting the shell in this venv,
# we don't have to import things we need to test every time.
def make_shell_context():
	return {'db' : db, 'User' : User, 'Chat' : Chat, 'Friendship' : Friendship}

if __name__ == '__main__' :
	socketio.run(app)


	
