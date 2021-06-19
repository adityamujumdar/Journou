from journou import db, login_manager
from time import gmtime, strftime
from flask_login import UserMixin

# function and decorater for reloading the user from the user.id stored in the session
@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

class Forums(db.Model):
	__tablename__ = 'forums'
	id = db.Column(db.Integer, primary_key=True)
	forum_name = db.Column(db.String(400), nullable=False)
	post_content = db.Column(db.Text)
	date_posted = db.Column(db.String(19), nullable=False, default=strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	likes = db.Column(db.Integer, nullable=False)
	dislikes = db.Column(db.Integer, nullable=False)
	forum_type = db.Column(db.String(3), nullable=False)
	posted_by = db.Column(db.String(15), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	# def __init__(self, forum_name, date_posted, posted_by, likes, dislikes, forum_type):
	# 	self.forum_name = forum_name
	# 	self.date_posted = date_posted
	# 	self.likes = likes
	# 	self.dislikes = dislikes
	# 	self.forum_type = forum_type
	# 	self.posted_by = posted_by

	def __repr__(self):
		return f"Forum('{self.id}', '{self.forum_name}', '{self.date_posted}')"

class Users(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False)
	email = db.Column(db.String(120), nullable=False)
	university = db.Column(db.Text(), nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.Text(), nullable=False)
	posts = db.relationship('Forums', backref='author', lazy=True)

	# def __init__(self, username, email, university, image_file, password):
	# 	self.username = username
	# 	self.email = email
	# 	self.university = university
	# 	self.image_file = image_file
	# 	self.password = password

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', {self.university}','{self.image_file}')"
		