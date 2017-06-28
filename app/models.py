from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(64), unique=True)
    person = db.Column(db.String(10))
    create_time = db.Column(db.DateTime)
    product_sub = db.relationship('Product_sub', backref='product', lazy='dynamic')

    def __init__(self, pro_name, create_time=None):
        self.pro_name = pro_name
        if create_time is None:
            create_time = datetime.now()
        self.create_time = create_time

    def __repr__(self):
        return "<Product %r>" % self.pro_name

class Product_sub(db.Model):
    __tablename__ = 'product_sub'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    package = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.now())
    last_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Product_sub %r>" % self.package