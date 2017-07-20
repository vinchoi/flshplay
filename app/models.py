from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(64), unique=True)
    person = db.Column(db.String(10))
    create_time = db.Column(db.DateTime, default=datetime.now())
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
    data_Date = db.Column(db.Date, default=date.today())
    create_time = db.Column(db.DateTime, default=datetime.now())
    last_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Product_sub %r>" % self.package

class User(db.Model):
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)