import secrets
import os
import json
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_asso import app, db, bcrypt
from flask_asso.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostRecette, Comments
from flask_asso.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required

''' Ce fichier permet de faire la gestion des url'''

@app.route('/') #Definit le chemin (url) vers la page
@app.route('/home')# On peux definir plusieur chemin vers une même route
def home():
    return render_template('index.html')

@app.route('/recettes')
def recettes():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=12, page=page)
	image_file = url_for('static', filename='recipe_pics/')
	return render_template('recettes.html',image_file=image_file, posts=posts)

@app.route('/layout')
def layout():
	return render_template('layout.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
	if current_user.is_authenticated:
		return(redirect(url_for('home')))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Echec de l\'authentification, veuillez verifier vos identifiants', 'red darken-3')
	return render_template('connexion.html', title='connexion', form=form)

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
	if current_user.is_authenticated:
		return(redirect(url_for('home')))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.pseudo.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Votre compte a été crée, vous pouvez maintenant vous connecté.', 'green lighten-3')
		return redirect(url_for('connexion'))
	return render_template('inscription.html', title='inscription', form=form)

@app.route('/deconnexion')
def deconnexion():
	logout_user()
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)

	return picture_fn

@app.route('/compte', methods=['GET', 'POST'])
@login_required
def compte():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.pseudo.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Votre compte a bien été mis a jour', 'green lighten-3')
		return redirect(url_for('compte'))
	elif request.method =='GET':
		form.pseudo.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
	return render_template('compte.html', title='compte', image_file=image_file, form=form)

def save_recipe(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/recipe_pics', picture_fn)

	output_size = (400, 400)
	i = Image.open(form_picture)
	i = i.resize(output_size)
	i.save(picture_path)

	return picture_fn

@app.route('/recettes/new', methods=['GET', 'POST'])
@login_required
def nouvelle_recette():
	form = PostRecette()
	if form.validate_on_submit():
		if Post.query.filter_by(title=form.title.data).first():
			flash('Une recette porte déjà ce nom', 'red darken-3')
			return redirect(url_for('nouvelle_recette'))
		if form.recipe.data:
			picture_recipe_file = save_recipe(form.recipe.data)
			post = Post(title=form.title.data, content=form.content.data, author=current_user, image_recipe=picture_recipe_file)
		else:
			print(form.content.data)
			post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Votre recette a bien été créé', 'green lighten-3')
		return redirect(url_for('home'))
	return render_template('new_recette.html', title='Nouvelle recette', form=form, legend='Nouvelles recette')

@app.route('/recette/<int:post_id>', methods=['GET', 'POST'])
def recette(post_id):
	form = Comments()
	post = Post.query.get_or_404(post_id)
	comments = Comment.query.filter_by(recette_id=post_id).order_by(Comment.date_posted.desc()).all()
	if form.validate_on_submit():
		comment = Comment(content=form.content.data, author_id=current_user.id, recette_id=post_id)
		db.session.add(comment)
		db.session.commit()
		flash('Votre commentaire a bien été créé', 'green lighten-3')
		return redirect(url_for('recette', post_id=post.id))
	profile_file = url_for('static', filename='profile_pics/')
	recipe_file = url_for('static', filename='recipe_pics/')
	return render_template('recette.html', title=post.title, profile_file=profile_file, recipe_file=recipe_file, post=post, form=form, comments=comments)

@app.route('/recette/<int:post_id>/update', methods=['GET', 'POST'])
def update_recipe(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	form = PostRecette()
	if form.validate_on_submit():
		if len(Post.query.filter_by(title=form.title.data).all())>1:
			flash('Une recette porte déjà ce nom', 'red darken-3')
			return redirect(url_for('update_recipe', post_id=post.id))
		post.title = form.title.data
		post.content= form.content.data
		if form.recipe.data:
			picture_recipe_file = save_recipe(form.recipe.data)
			post.image_recipe = picture_recipe_file
		db.session.commit()
		flash('Votre recette a été mise à jour', 'green lighten-3')
		return redirect(url_for('recette', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		for post_content in post.content:
			form.content.append_entry(post_content)
	return render_template('new_recette.html', form=form, legend='Mettre à jour la recette')

@app.route('/recette/<int:post_id>/delete', methods=['POST'])
def delete_recipe(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Votre recette a bien été supprimé', 'green lighten-3')
	return redirect(url_for('recettes'))

@app.route('/compte/<string:username>')# On peux definir plusieur chemin vers une même route
def  compte_recette(username):
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(per_page=12, page=page)
	image_file = url_for('static', filename='recipe_pics/')
	return render_template('compte_recette.html',image_file=image_file, posts=posts, user=user)

#Suppression de commentaire
@app.route('/recette/<int:post_id>/delete_com/<int:comment_id>', methods=['POST'])
def delete_com(comment_id, post_id):
	comment = Comment.query.get_or_404(comment_id)
	if comment.author != current_user:
		abort(403)
	db.session.delete(comment)
	db.session.commit()
	flash('Le commentaire a bien été supprimé', 'green lighten-3')
	return redirect(url_for('recette', post_id=post_id))

#Suppression de compte
@app.route('/compte/delete', methods=['POST'])
@login_required
def delete_account():
	account = User.query.get_or_404(current_user.id)
	logout_user()
	db.session.delete(account)
	db.session.commit()
	flash('Votre compte à bien été supprimé', 'green lighten-3')
	return redirect(url_for('home'))

#Genère une erreur 404 sur les pages qui n'existent pas
@app.errorhandler(404)
def page_not_found(e):
	return render_template('errors.html', error= "404", msg= "Page non trouvé"), 404