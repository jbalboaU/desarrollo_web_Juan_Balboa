from flask import Flask
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__, template_folder='templates')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.secret_key = 'ZGVzYXJyb2xsb19fd2Vi'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    db.init_app(app)

    from routes import register_routes
    register_routes(app,db)

    migrate = Migrate(app, db)

    return app