from flask import flash, redirect, request, jsonify, url_for
from flask import render_template
from flask_paginate import Pagination
from googletrans import Translator
from flask_login import login_required, login_user, logout_user
from models import Profile, PostCategory, Post
from app import db


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

    @app.route('/login', methods=['GET', 'POST'])
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

    @app.route('/register', methods=['GET', 'POST'])
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