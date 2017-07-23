#coding:utf-8

from . import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

class Permission:
    look = 0x01  # 查看
    add = 0x02  # 新增
    edit = 0x04  # 编辑
    delete = 0x08  # 删除
    ADMINISTER = 0x80  # 管理员权限

# 中间表
registrations = db.Table('registrations',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String)
   classes = db.relationship('Class',secondary=registrations,
                                    backref=db.backref('students', lazy='dynamic'),
                                    lazy='dynamic')


class Class(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)



class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(64), unique=True)
    person = db.Column(db.String(10))
    create_time = db.Column(db.DateTime(), default=datetime.now)
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
    create_time = db.Column(db.DateTime(), default=datetime.now)
    last_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<Product_sub %r>" % self.package

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'guest': (Permission.look, False),
            'User': (Permission.look | Permission.add | Permission.edit | Permission.delete, True),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(role_name=r).first()
            if role is None:
                role = Role(role_name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

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

    def can(self, permissions):
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __repr__(self):
        return "<User %r>" % self.username



''' 未登录用户的控制
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

'''

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
