from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from werkzeug.security import generate_password_hash
import secrets
import os

secret = secrets.token_urlsafe(32)

SQL_DIR = 'db_data'

DB_USER = 'root'
DB_PASSWORD = '12345678'
DB_HOST = 'localhost'
DB_PORT = '3306'

ADMIN_USER = 'admin'
ADMIN_PASSWORD = 'admin'

if 'DB_HOST' in os.environ.keys():
    DB_HOST = os.environ.get('DB_HOST')
if 'DB_PORT' in os.environ.keys():
    DB_PORT = os.environ.get('DB_PORT')
if 'ADMIN_USER' in os.environ.keys():
    DB_PORT = os.environ.get('ADMIN_USER')
if 'ADMIN_PASSWORD' in os.environ.keys():
    DB_PORT = os.environ.get('ADMIN_PASSWORD')

app = Flask(__name__)
app.config['SECRET_KEY'] = secret  # для авторизации
app.config['SQLALCHEMY_DATABASE_URI'] = \
    f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/flask?allow_local_infile=1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # для экономии памяти

db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

admin_panel = Admin(app, name='Админ панель', template_mode='bootstrap4')

from views import init_views, ProfileAdmin, PostCategoryAdmin, PostAdmin, TrainDataAdmin
from models import Profile, PostCategory, Post, TrainData


@app.cli.command('create_initial_admin')
def create_initial_admin():
    print('Создание супер-пользователя...')
    admin = Profile(id=1, user=ADMIN_USER, password=generate_password_hash(ADMIN_PASSWORD), is_admin=True)
    db.session.add(admin)
    db.session.commit()

@app.cli.command('load_data')
def load_data():
    print('Загрузка первоначальных данных в БД...')
    tables = ['postcategory', 'post', 'traindata']
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


init_views(app)

admin_panel.add_view(ProfileAdmin(Profile, db.session))
admin_panel.add_view(PostCategoryAdmin(PostCategory, db.session))
admin_panel.add_view(PostAdmin(Post, db.session))
admin_panel.add_view(TrainDataAdmin(TrainData, db.session))

if __name__ == '__main__':
    app.run()
