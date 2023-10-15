from flask import Flask, request
from flask import render_template
from flask_migrate import Migrate
from flask_paginate import Pagination
from database import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345678@localhost:3306/flask'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    posts = Post.query.all()
    page = request.args.get('page', 1, type=int)
    per_page = 3
    pagination = Pagination(page=page, total=len(posts), per_page=per_page)
    start_ind = (page - 1) * per_page
    end_ind = start_ind + per_page
    posts_to_render = posts[start_ind:end_ind]
    return render_template('home.html', pagination=pagination, posts=posts_to_render)


@app.route('/post')
def post():
    requested_id = request.args.get('id', 1, type=int)
    post = Post.query.filter_by(id=requested_id).first()
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run()
