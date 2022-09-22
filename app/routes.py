from typing_extensions import Self
from wsgiref.validate import validator
from flask import render_template, flash, redirect, url_for, request
from app import app, query_db, login, test_query
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm
from datetime import datetime
from passlib.hash import pbkdf2_sha256
from flask_login import current_user, login_user, login_required, logout_user
import os
import json

# this file contains all the different routes, and the logic for communicating with the database

class User():
    def __init__(self,id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.authenticated = False
    def is_active(self):
         return self.is_active()
    def is_anonymous(self):
         return False
    def is_authenticated(self):
         return self.authenticated
    def is_active(self):
         return True
    def get_id(self):
         return self.id
@login.user_loader
def load_user(id):
    user=query_db('SELECT * FROM Users WHERE id="{}";'.format(id), one=True)
    return User(user['id'],user['username'],user['password'])

    
# home page/login/registration
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('stream', username=current_user.username))
    form = IndexForm()

    if form.login.validate_on_submit():
        user = query_db('SELECT * FROM Users WHERE username="{}";'.format(form.login.username.data), one=True)
        if user == None or not pbkdf2_sha256.verify(form.login.password.data, user['password']): #verify password and username
            flash('Sorry, wrong username or password!')
        else:
            us = load_user(user['id'])
            login_user(us,remember=form.login.remember_me.data)
            return redirect(url_for('stream'))
    elif form.register.validate_on_submit():
        #hashing
        if query_db('INSERT INTO Users (username, first_name, last_name, password) VALUES("{}", "{}", "{}", "{}");'.format(form.register.username.data, form.register.first_name.data, form.register.last_name.data, pbkdf2_sha256.hash(form.register.password.data)))==0:
           #printer feilmelding hvis bruker eksisterer fra før
            flash('User already exists!')
        else:
            flash('User created successfully!')
            return redirect(url_for('index'))
    elif form.register.submit.data:
        flash('User not created!')
    elif form.login.submit.data:
        flash('Login failed!')
        
    return render_template('index.html', title='Welcome', form=form)
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# content stream page
@app.route('/stream', methods=['GET', 'POST'])
@login_required
def stream():
    form = PostForm()
    
    if form.validate_on_submit():
        if form.image.data:
            path = os.path.join(app.config['UPLOAD_PATH'], form.image.data.filename)
            form.image.data.save(path)


        query_db('INSERT INTO Posts (u_id, content, image, creation_time) VALUES({}, "{}", "{}", \'{}\');'.format(current_user.id, form.content.data, form.image.data.filename, datetime.now()))
        return redirect(url_for('stream'))

    posts = query_db('SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id={0}) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id={0}) OR p.u_id={0} ORDER BY p.creation_time DESC;'.format(current_user.id))
    return render_template('stream.html', title='Stream', form=form, posts=posts)

# comment page for a given post and user.
@app.route('/comments/<int:p_id>', methods=['GET', 'POST'])
@login_required
def comments(p_id):
    if not test_query('SELECT id FROM Posts WHERE id="{}";'.format(p_id)):
        flash('This post doesnt exist!')
        return redirect(url_for('stream'))
    form = CommentsForm()
    if form.validate_on_submit():
        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES({}, {}, "{}", \'{}\');'.format(p_id, current_user.id, form.comment.data, datetime.now()))

    post = query_db('SELECT * FROM Posts JOIN Users ON Posts.u_id=Users.id WHERE Posts.id={};'.format(p_id), one=True)
    all_comments = query_db('SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id={} ORDER BY c.creation_time DESC;'.format(p_id))
    return render_template('comments.html', title='Comments', form=form, post=post, comments=all_comments)

# page for seeing and adding friends
@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    form = FriendsForm()
    all_friends = query_db('SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id={} AND f.f_id!={} ;'.format(current_user.id, current_user.id))
    if form.validate_on_submit():
        
        friend = query_db('SELECT * FROM Users WHERE username="{}";'.format(form.username.data), one=True)
        if friend is None:
            flash('User does not exist')
        elif friend['id']==current_user.id:
            flash('Why you wanna add yourself??')
        elif any(friend['id'] in x for x in all_friends):
            flash('Already friends!')
        else:
            query_db('INSERT INTO Friends (u_id, f_id) VALUES({}, {});'.format(current_user.id, friend['id']))  
            flash('Friend added!') 
            return redirect(url_for('friends'))

    
    return render_template('friends.html', title='Friends', friends=all_friends, form=form)

# see and edit detailed profile information of a user
@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    form = ProfileForm()
    if form.validate_on_submit():
      
        query_db('UPDATE Users SET education="{}", employment="{}", music="{}", movie="{}", nationality="{}", birthday=\'{}\' WHERE username="{}" ;'.format(
            form.education.data, form.employment.data, form.music.data, form.movie.data, form.nationality.data, form.birthday.data, current_user.username
        ))
        return redirect(url_for('profile', username=current_user.username))
    
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    return render_template('profile.html', title='profile', username=username,user=user, form=form)