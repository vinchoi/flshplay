from . import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(64))
    person = db.Column(db.String(10))
    create_time = db.Column(db.DateTime, default=datetime.now())
    create_by = db.Column(db.Integer)
    product_sub = db.relationship('Product_sub', backref='product', lazy='dynamic')

    # def __init__(self, pro_name, create_time=None):
    #     self.pro_name = pro_name
    #     if create_time is None:
    #         create_time = datetime.now()
    #     self.create_time = create_time

    def __repr__(self):
        return "<Product %r>" % self.pro_name

class Product_sub(db.Model):
    __tablename__ = 'product_sub'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    package = db.Column(db.Integer, default=0)
    data = db.Column(db.Integer, default=0)
    data_Date = db.Column(db.Date)
    create_time = db.Column(db.DateTime)
    last_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Product_sub %r>" % self.package

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.role_name

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
