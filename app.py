from flask import Flask
from flask_migrate import Migrate
from database import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:12345678@localhost:3306/flask'
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
