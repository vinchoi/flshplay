#coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DateTimeField, TextAreaField, DateField
from wtforms.validators import length, DataRequired
from ..models import Product, Product_sub

class AddProduct(FlaskForm):
    pro_name = StringField(u'产品名称', validators=[DataRequired()])
    person = StringField(u'对接人', validators=[DataRequired()])
    submit = SubmitField(u'保存')


class EditProduct(AddProduct):
    product_id = StringField(validators=[DataRequired()])


class DeleteProductForm(FlaskForm):
    productId = StringField(validators=[DataRequired()])


class ManagePackageForm(FlaskForm):
    product = SelectField(u'产品', coerce=int)
    submit = SubmitField(u'筛选')


class AddPackage(FlaskForm):
    pro_id = SelectField(u'产品', coerce=int)
    package = IntegerField(u'包号', validators=[DataRequired()])
    data = IntegerField(u'数据', validators=[DataRequired()])
    data_Date = DateField(u'数据日期', validators=[DataRequired()])
    submit = SubmitField(u'保存')

    def __init__(self, *args, **kwargs):
        super(AddPackage, self).__init__(*args, **kwargs)
        self.pro_id.choices = [(pro.id, pro.pro_name) for pro in Product.query.all()]


class EditPackage(AddPackage):
    package_id = StringField(validators=[DataRequired()])


class DeletePackageForm(FlaskForm):
    packageId = StringField(validators=[DataRequired()])


#  用于数据查看页
class SearchForm(FlaskForm):
    begin_time = DateField(u'开始时间:')
    end_time = DateField(u'结束时间:')
    submit = SubmitField(u'搜索')