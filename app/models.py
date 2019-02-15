import os
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import db, login_manager


secret = os.getenv('SECRET_KEY')


class User(UserMixin, db.Model):
    """
    Class for creating user tables on db
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(50), index=True, nullable=False)
    last_name = db.Column(db.String(50), index=True, nullable=False)
    id_number = db.Column(db.String(20), index=True, nullable=False)
    phone_number = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(1000), nullable=False,
                           default='default.jpg')
    is_transporter = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    cargo_routes = db.relationship('CargoRoutes', backref='routes',
                                   lazy=True, cascade='all, delete-orphan')
    drivers = db.relationship(
        'Drivers', backref='driver', lazy=True, cascade='all, delete-orphan')
    vehicles = db.relationship(
        'Vehicles', backref='vehicle', lazy=True, cascade='all, delete-orphan')

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual one
        """
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(secret, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(secret)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

# set up a user loader


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class CargoRoutes(db.Model):
    """
    Class creates tables for details regarding routes
    """

    __tablename__ = 'cargo routes'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    start_point = db.Column(db.Text, nullable=False)
    destination = db.Column(db.Text, nullable=False)
    from_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    to_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    image_file = db.Column(db.String(1000), nullable=True,
                           default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Drivers(db.Model):
    """
    Class creates tables for details regarding routes
    """

    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(250), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(50), index=True, nullable=False)
    middle_name = db.Column(db.String(50), index=True, nullable=False)
    last_name = db.Column(db.String(50), index=True, nullable=False)
    id_number = db.Column(db.String(20), index=True, nullable=False)
    phone_number = db.Column(db.String(100), index=True, nullable=False)
    license_number = db.Column(db.String(100), index=True, nullable=False)
    image_file = db.Column(db.String(1000), nullable=False,default='default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Vehicles(db.Model):
    """
    Class creates tables for details regarding routes
    """

    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    registration_number = db.Column(db.String(20), index=True, nullable=False)
    vehicle_type = db.Column(db.String(100), index=True, nullable=False)
    inspection_sticker = db.Column(db.String(100), index=True, nullable=False)
    load_capacity = db.Column(db.String(20), index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

