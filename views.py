from flask import flash, redirect, request, jsonify, url_for, abort
from flask import render_template
from flask_admin import AdminIndexView
from flask_paginate import Pagination
from googletrans import Translator
from flask_login import login_required, login_user, logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from models import Profile, PostCategory, Post, PredData
from app import db
from ml import train_model, predict_model
import shutil


def init_views(app):
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

    @app.route('/topic', methods=['GET'])
    def topic():
        requested_topic_id = request.args.get('id', 1, type=int)
        current_topic = PostCategory.query.filter_by(id=requested_topic_id).first()
        page = request.args.get('page', 1, type=int)
        posts = Post.query.filter_by(category=requested_topic_id).all()
        per_page = 2
        pagination = Pagination(page=page, total=len(posts), per_page=per_page)
        start_ind = (page - 1) * per_page
        end_ind = start_ind + per_page
        posts_to_render = posts[start_ind:end_ind]
        return render_template('topic.html', pagination=pagination, posts=posts_to_render, topic=current_topic)

    @app.route('/post', methods=['GET'])
    def post():
        requested_id = request.args.get('id', 1, type=int)
        post = Post.query.filter_by(id=requested_id).first()
        return render_template('post.html', post=post)

    @app.route('/search', methods=['GET'])
    def search():
        key = request.args.get('query')
        posts = Post.query.msearch(key, fields=['title', 'body'])
        page = request.args.get('page', 1, type=int)
        per_page = 3
        pagination = Pagination(page=page, total=len(posts), per_page=per_page)
        start_ind = (page - 1) * per_page
        end_ind = start_ind + per_page
        posts_to_render = posts[start_ind:end_ind]
        return render_template('search.html', pagination=pagination, posts=posts_to_render, query=key)

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

    @app.route('/train', methods=['GET', 'POST'])
    def train():
        if request.method == 'POST':
            train_model()
            return jsonify({'status': 'OK'})
        return render_template('train_page.html')

    @app.route('/predict', methods=['POST'])
    def predict():
        if request.method == 'POST':
            age = int(request.form.get('age'))
            sex = int(request.form.get('sex'))
            bmi = float(request.form.get('bmi'))
            children = int(request.form.get('children'))
            smoker = bool(request.form.get('smoker'))
            charges = float(predict_model(age, sex, bmi, children, smoker))
            new_pred = PredData(age=age, sex=sex, bmi=bmi, children=children, smoker=smoker, charges=charges)
            db.session.add(new_pred)
            db.session.commit()
            return jsonify({'result': "${:,.2f}".format(charges)})

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == "POST":
            user = Profile.query.filter_by(user=request.form.get("user")).first()
            if user is None:
                if request.form.get("fromModal"):
                    return jsonify({'error': 'Пользователь не найден'})
                else:
                    flash('Пользователь не найден')
                    return render_template('login.html')
            if check_password_hash(user.password, request.form.get("password")):
                login_user(user)
                if request.form.get("fromModal"):
                    return jsonify({'success': 'true'})
                else:
                    return redirect(url_for("home"))
            else:
                if request.form.get("fromModal"):
                    return jsonify({'error': 'Неправильный пароль'})
                else:
                    flash('Неверный логин или пароль')
                    return render_template('login.html')
        else:
            return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == "POST":
            user = request.form.get("user")
            password = request.form.get("password")
            submit = request.form.get("password2")
            is_modal = True if request.form.get('fromModal') else False
            user_profile = Profile.query.filter_by(user=user).first()
            if user_profile:
                flash('Пользователь уже существует')
                return jsonify({'error': 'Пользователь уже существует'}) if is_modal else redirect(url_for('register'))
            if password != submit:
                flash('Пароли не совпадают')
                return jsonify({'error': 'Пароли не совпадают'}) if is_modal else redirect(url_for('register'))
            new_user = Profile(user=user, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            shutil.copy('./static/defaultAvatar.png', f'./static/avatars/{user}.png')
            flash('Успешная регистрация')
            return jsonify({'success': 'true'}) if is_modal else redirect(url_for("login"))
        else:
            return render_template('register.html')

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route('/upload_avatar', methods=['POST'])
    @login_required
    def upload_avatar():
        if request.files['avatar']:
            image = request.files['avatar']
            image.save(f'./static/avatars/{current_user.user}.png')
        return redirect(url_for("home"))


class CustomAdminView(AdminIndexView):
    def is_accessible(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Запретить доступ к административной панели
        return True


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


class ProfileAdmin(AdminModelView):
    column_list = ('id', 'user', 'password')
    column_labels = {'id': 'ID', 'user': 'Логин', 'passwords': 'Пароль'}


class PostCategoryAdmin(AdminModelView):
    column_list = ('id', 'title')
    column_labels = {'id': 'ID', 'title': 'Название категории'}


class PostAdmin(AdminModelView):
    column_list = ('id', 'title', 'category', 'author', 'body')
    column_labels = {'id': 'ID', 'title': 'Заголовок', 'category': 'Категория', 'author': 'Автор', 'body': 'Текст'}


class TrainDataAdmin(AdminModelView):
    column_list = ('id', 'age', 'sex', 'bmi', 'children', 'smoker', 'charges')
    column_labels = {'id': 'ID', 'age': 'Возраст', 'sex': 'Пол', 'bmi': 'ИМТ', 'children': 'Дети', 'smoker': 'Курит',
                     'charges': 'Плата'}
