from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app import *


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://:@/'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(256))
	avatar = db.Column(db.LargeBinary)

	def __init__(self, *args, **kwargs):
		super(Profile,self).__init__(*args,**kwargs)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200))
	category = db.Column(db.Integer, db.ForeignKey("postcategory.id"))
	author = db.Column(db.Integer, db.ForeignKey("profile.id"))
	body = db.Column(db.Text)

class PostCategory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))

class MLData(db.Model):
	# sexField = [
    #     (0, "Женщина"),
    #     (1, "Мужчина"),
    # ]
	id = db.Column(db.Integer, primary_key=True)
	age = db.Column(db.Integer, blank=False)
	sex = db.Column(db.Boolean, blank=False)
	bmi = db.Column(db.Float, blank=False)
	children = db.Column(db.Integer, blank=False)
	smoker = db.Column(db.Boolean, blank=False)
	charges = db.Column(db.Float, blank=False)

	__abstract__ = True

class TrainData(MLData):
    pass


class PredictedData(MLData):
    pass
