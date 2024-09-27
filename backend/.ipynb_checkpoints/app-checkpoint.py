#!/usr/bin/env python
# coding: utf-8

# In[1]:

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


# In[3]:


app = Flask(__name__)
app.config['SECRET_KEY'] = "JPMorgan123!"
db_path = os.path.join(os.path.dirname(__file__), 'database', 'Blog Platform Database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# In[5]:


db = SQLAlchemy(app)


# In[7]:


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.Enum('Admin', 'Author', 'Reader'), default='Reader')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# In[9]:


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    category = db.Column(db.String(100))
    tags = db.Column(db.Text)


# In[11]:


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# In[13]:


class Tag(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(100), unique=True, nullable=False)


# In[15]:


class PostTag(db.Model):
    post_tag_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.tag_id'))


# In[17]:


with app.app_context():
    db.create_all()


# In[19]:


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


# In[21]:


@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post_detail.html', post=post, comments=comments)


# In[23]:


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.user_id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed!', 'Check your credentials', 'danger')
    return render_template('login.html')


# In[25]:


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password_hash=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment_route(post_id):
    return add_comment(post_id)

# In[27]:

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' in session:
        comment_text = request.form['comment']
        new_comment = Comment(post_id=post_id, user_id=session['user_id'], comment=comment_text)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    else:
        flash('You need to be logged in to comment', 'danger')
    return redirect(url_for('post_detail', post_id=post_id))


# In[29]:


if __name__ == '__main__':
    app.run(debug=True)

