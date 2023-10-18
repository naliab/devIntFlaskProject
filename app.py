import secrets
secret = secrets.token_urlsafe(32)

from flask import Flask, flash, redirect, request, jsonify, url_for
from flask import render_template
from flask_migrate import Migrate
from flask_paginate import Pagination
from googletrans import Translator
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash,  check_password_hash

app = Flask(__name__)
app.secret_key = secret # Для авторизации

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345678@localhost:3306/flask'
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

class Profile(db.Model, UserMixin):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(256))
    avatar = db.Column(db.String(256))

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(Profile).get(user_id)

class PostCategory(db.Model):
    __tablename__ = 'postcategory'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    category = db.Column(db.Integer, db.ForeignKey("postcategory.id"))
    author = db.Column(db.Integer, db.ForeignKey("profile.id"))
    body = db.Column(db.Text)
    categoryParent = db.relationship('PostCategory', backref='children')
    authorParent = db.relationship('Profile', backref='children')


class MLData(db.Model):
    # sexField = [
    #     (0, "Женщина"),
    #     (1, "Мужчина"),
    # ]
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer)
    sex = db.Column(db.Boolean)
    bmi = db.Column(db.Float)
    children = db.Column(db.Integer)
    smoker = db.Column(db.Boolean)
    charges = db.Column(db.Float)

    __abstract__ = True


class TrainData(MLData):
    pass


class PredictedData(MLData):
    pass


@app.route('/', methods=['GET'])
def home():
    posts = Post.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = 3
    pagination = Pagination(page=page, total=len(posts), per_page=per_page)
    start_ind = (page - 1) * per_page
    end_ind = start_ind + per_page
    posts_to_render = posts[start_ind:end_ind]
    return render_template('home.html', pagination=pagination, posts=posts_to_render)


@app.route('/post', methods=['GET'])
def post():
    requested_id = request.args.get('id', 1, type=int)
    post = Post.query.filter_by(id=requested_id).first()
    return render_template('post.html', post=post)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/translate', methods=['POST'])
def translate():
    target_lang = 'en'
    title = request.form.get('title')
    body = request.form.get('txt')

    translator = Translator()
    title_result = translator.translate(title, dest=target_lang)
    body_result = translator.translate(body, dest=target_lang)

    return jsonify({'title_translation': title_result.text, 'txt_translation': body_result.text})

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        user = Profile.query.filter_by(user=request.form.get("user")).first()
        if user is None:
            flash('Неверный логин или пароль')
            return render_template('login.html')
        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        user = request.form.get("user")
        password = request.form.get("password")

        user_profile = Profile.query.filter_by(user=user).first() 
        if user_profile: 
            flash('Пользователь уже существует')
            return redirect(url_for('register'))
        
        new_user = Profile(user=user, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template('register.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()
