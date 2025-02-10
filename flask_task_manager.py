from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.secret_key = '888573cf6a0ea8ec8404c71fc21ab2aea4b80654789126e2ecd2acd1366426a0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

from models import db
db.init_app(app) 

from auth.routes import auth_bp
from tasks.routes import tasks_bp

app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)

@app.route('/')
def welcome():
    return "Welcome to the Flask Task Manager! Please <a href='/login'>log in</a> or <a href='/register'>register</a>."

if __name__ == '__main__':
    with app.app_context(): 
        db.create_all()
    app.run(debug=True)
