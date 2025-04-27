from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
from app.models import Transaction
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()  # Initialize Flask-Mail

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    # Setting the secret key (ensure your config or environment contains a good secret key)
    app.secret_key = app.config.get('SECRET_KEY', 'supersecretkey')

    # Initialize the database with the app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    mail.init_app(app)  # Initialize Flask-Mail with the app

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main
    from app.auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
