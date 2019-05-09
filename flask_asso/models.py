from flask_asso import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from random import randint

""" Ce fichier permet de crée une base de donnée """

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default'+ str(randint(1, 9))+'.jpg')
	password = db.Column(db.String(60), nullable=False)

	posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
	comment = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete-orphan")


	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(100), unique=True, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
	content = db.Column(db.PickleType(), nullable=False)
	image_recipe = db.Column(db.String(20), nullable=False, default='recipe.jpg')
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	comments = db.relationship('Comment', backref='recette', lazy=True, cascade="all, delete-orphan")

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	content = db.Column(db.Text, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
	recette_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

	def __repr__(self):
		return f"Comment('{self.id}', '{self.user_id}', {self.recette_id})"