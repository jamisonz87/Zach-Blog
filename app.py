from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired
from flaskext.markdown import Markdown

app = Flask(__name__)

app.config.from_pyfile('config.cfg')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Markdown(app, extensions=['fenced_code'])

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='user', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    post = db.Column(db.String(20000))
    mark_url = db.Column(db.String(50))
    post_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class LoginForm(FlaskForm):
    username = StringField('Enter Username', validators=[InputRequired("Please Enter Username")])
    password = PasswordField('Enter Password', validators=[InputRequired("Please Enter Password")])

class PostForm(FlaskForm):
    title = StringField('Enter Title', validators=[InputRequired("Please Enter a Title")])
    post = StringField('', validators=[InputRequired("Please Enter Url")])

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()

@app.route('/')
def index():
    current_posts_list = []
    
    all_posts = Post.query.filter().order_by(Post.id.desc())

    for p in all_posts:
        current_post = {}
        
        content = ""
        with open('static/markdown/{}'.format(p.mark_url), 'r') as f:
            content = f.read()

        current_post['subject'] = p.subject
        current_post['post'] = content
        current_post['post_date'] = p.post_date
        user = User.query.filter_by(id=p.user_id).first()
        current_post['id'] = p.id
        current_post['user_id'] = user.username

        current_posts_list.append(current_post)

    return render_template('index.html', posts=current_posts_list)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = ''

    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
               error = 'Username or password is incorrect'
        else:
            error = 'Username or password is incorrect'

    return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(subject=form.title.data, mark_url=form.post.data, post_date=datetime.now(), user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('post.html', form=form)

'''
@app.route('/create')
def create():
    new_user = User(username='', password=generate_password_hash('','sha256'))
    db.session.add(new_user)
    db.session.commit()
'''


if __name__ == '__main__':
    app.run(debug=True)