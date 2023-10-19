import secrets
from flask_login import LoginManager

from flask_sqlalchemy import SQLAlchemy
secret = secrets.token_urlsafe(32)
from flask import Flask
from flask_migrate import Migrate
from flask_paginate import Pagination
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
app.secret_key = secret # Для авторизации
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

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

from views import init_views
init_views(app)

if __name__ == '__main__':
    app.run()
