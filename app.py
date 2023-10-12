from flask import Flask
from flask import render_template,flash,redirect,session,request,jsonify
# from loginform import *
# from database import *

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
