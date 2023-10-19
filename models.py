from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Profile(db.Model, UserMixin):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(256))

    def __init__(self, *args, **kwargs):
        super(Profile, self).__init__(*args, **kwargs)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
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
    __tablename__ = 'traindata'
    pass


class PredData(MLData):
    __tablename__ = 'preddata'
    pass
