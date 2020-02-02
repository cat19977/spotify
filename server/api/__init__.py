from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)



    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

    db.init_app(app)
    
    from .login import main  
    app.register_blueprint(main)


    return app
