#coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateTimeField
from wtforms.validators import length, DataRequired
from ..models import Product, Product_sub


class AddProduct(FlaskForm):
    pro_name = StringField(u'产品名称', validators=[DataRequired()])
    # creat_time = DateTimeField()
    submit = SubmitField(u'保存')


class AddPackage(FlaskForm):
    pro_name = SelectField(u'产品名称', coerce=int)
    package = IntegerField(u'包号', validators=[DataRequired()])
    last_time = DateTimeField()
    submit = SubmitField(u'保存')

    def __init__(self, *args, **kwargs):
        super(AddPackage, self).__init__(*args, **kwargs)
        self.pro_name.choices = [(pro.id, pro.pro_name) for pro in Product.query.all()]
