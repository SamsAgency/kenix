# app/__init__.py

# third party imports

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
from flask_mail import Mail

# local imports

from instance.config import app_config

# initialize the db variable

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()


def create_app(config_name):
    """
    create_app function that, given a configuration name, loads the correct configuration from the
    config.py file, as well as the configurations from the instance/config.py
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.url_map.strict_slashes = False
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this space"
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)
    Bootstrap(app)
    Markdown(app, auto_escape=True)
    mail.init_app(app)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .transporter import transporter as transporter_blueprint
    app.register_blueprint(transporter_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
