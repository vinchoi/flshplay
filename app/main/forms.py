#coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateTimeField, TextAreaField, DateField
from wtforms.validators import length, DataRequired
from ..models import Product, Product_sub


class AddProduct(FlaskForm):
    pro_name = StringField(u'产品名称', validators=[DataRequired()])
    person = StringField(u'对接人', validators=[DataRequired()])
    submit = SubmitField(u'保存')


class AddPackage(FlaskForm):
    pro_id = SelectField(u'产品', coerce=int)
    package = IntegerField(u'包号', validators=[DataRequired()])
    data = IntegerField(u'数据', validators=[DataRequired()])
    data_Date = DateField(u'数据日期', validators=[DataRequired()])
    submit = SubmitField(u'保存')

    def __init__(self, *args, **kwargs):
        super(AddPackage, self).__init__(*args, **kwargs)
        self.pro_id.choices = [(pro.id, pro.pro_name) for pro in Product.query.all()]


class SearchView(FlaskForm):
    pro_name = TextAreaField()
    person = TextAreaField()
    package = TextAreaField()
    last_time = TextAreaField()
    submit = SubmitField(u'搜索')