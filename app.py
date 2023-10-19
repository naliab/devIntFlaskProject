from flask import Flask, request, jsonify
from flask import render_template
from flask_migrate import Migrate
from flask_paginate import Pagination
from database import *
from googletrans import Translator
from sqlalchemy import text
import os

SQL_DIR = 'db_data'

DB_USER = 'root'
DB_PASSWORD = '12345678'
DB_HOST = 'localhost'
DB_PORT = '3306'

if 'DB_HOST' in os.environ.keys():
    DB_HOST = os.environ.get('DB_HOST')
if 'DB_PORT' in os.environ.keys():
    DB_PORT = os.environ.get('DB_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/flask?allow_local_infile=1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # для экономии памяти

db.init_app(app)
migrate = Migrate(app, db)


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


@app.cli.command('load_data')
def load_data():
    print('Загрузка первоначальных данных в БД...')
    tables = ['profile', 'postcategory', 'post']
    for table_name in tables:
        file = SQL_DIR + '/' + table_name + '.csv'
        print('загрузка', file)
        with open(file, 'r', encoding='utf-8') as f:
            columns = f.readline().strip('\n').replace(';', ',')
            db.session.execute(text(
                f"LOAD DATA LOCAL INFILE '{file}' INTO TABLE {table_name} FIELDS TERMINATED BY ';'"
                f"OPTIONALLY ENCLOSED BY '\"' IGNORE 1 LINES ({columns})"
            ))
            db.session.commit()


if __name__ == '__main__':
    app.run()
