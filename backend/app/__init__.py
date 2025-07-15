from flask import Flask 
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from os import path
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

DB_NAME = "DataBase.db"

def create_app ():
    app = Flask(__name__)
    CORS(app=app)

    app.config['SECRET_KEY'] = "Mine"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(app.instance_path, DB_NAME)}'

    with app.app_context():
        if not path.exists(app.instance_path):
            os.makedirs(app.instance_path)

    db.init_app(app)
    migrate.init_app(app,db)

    from .views import views
    create_database(app)

    app.register_blueprint(views,url_prefix='/')

    return app;

def create_database(app):
    db_path = path.join(app.instance_path, DB_NAME)
    print(f"Checking for database at: {db_path}")

    if not path.exists(db_path):
        with app.app_context():
            db.create_all()  # Create tables based on the models
        print("DATABASE CREATED SUCCESSFULLY!")
    else:
        print("DATABASE ALREADY EXISTS!")