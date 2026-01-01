from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from socket import gethostname

# Initialize SQLAlchemy instance (outside create_app for import access)
db = SQLAlchemy()
DB_USER = "ntoutloff"
DB_PW = "mysql1986"
DB_HOST = f"{DB_USER}.mysql.pythonanywhere-services.com"
DB_NAME = f"{DB_USER}$go_gift"


def create_app():
    app = Flask(__name__)
    
    # Configuration
    if gethostname() != 'blue-liveweb48': # If not running on pythonanywhere, use local sqlite db
        app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    else:
        app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PW}@{DB_HOST}:3306/{DB_NAME}'
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 280, 'connect_args': {'connect_timeout': 5}}

    # Initialize extensions with app
    db.init_app(app)
    
    from . import models
    
    with app.app_context():
        db.create_all()
        print('Created Database!')
    
    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # User loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app