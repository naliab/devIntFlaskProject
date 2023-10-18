import secrets
secret = secrets.token_urlsafe(32)
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = secret # Для авторизации
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345678@localhost:3306/flask'
db = SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

from views import init_views
init_views(app)


if __name__ == '__main__':
    app.run()
