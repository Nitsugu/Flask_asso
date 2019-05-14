from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_asso.models import User

""" Ce fichier permet de crée des formulaire """

class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""
	pseudo = StringField('Pseudo',
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Adresse mail', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Mot de passe', 
		validators=[DataRequired()])
	confirm_password = PasswordField('Confirmer le mot de passe', 
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Inscription')

	def validate_pseudo(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Ce nom d\'utilisateur est déjà pris, veuillez en choisir un autres')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Ce email est déjà pris, veuillez en choisir un autres')

class LoginForm(FlaskForm):
	"""docstring for RegistrationForm"""
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Mot de passe', 
		validators=[DataRequired()])
	remember = BooleanField('Se souvenir de moi')
	submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
	"""docstring for UpdateAccountForm"""
	pseudo = StringField('Pseudo',
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Adresse mail', 
		validators=[DataRequired(), Email()])
	picture = FileField('Changer l\'image de profile', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Mettre à jour')

	def validate_pseudo(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Ce nom d\'utilisateur est déjà pris, veuillez en choisir un autres')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Ce email est déjà pris, veuillez en choisir un autres')

class PostRecette(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = FieldList(TextAreaField('Etape', validators=[DataRequired()]), min_entries=1, max_entries=20)
	recipe = FileField('Mettre une image de recette', validators=[FileAllowed(['jpg','png'])])
	submit = SubmitField('Post')

class Comments(FlaskForm):
	content = StringField('Commentaire', validators=[DataRequired()])
	submit = SubmitField('Poster le Commentaire')