#coding:utf-8

from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from .forms import AddProduct, AddPackage, SearchView

from . import main
from .. import db
from ..models import Product_sub, Product

@main.route('/')
@main.route('/index.html', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/new-user.html', methods=['GET', 'POST'])
def personal_info():
    return render_template('new-user.html')

@main.route('/t-addpro.html', methods=['GET', 'POST'])
def taddpro():
    form = AddProduct()
    if form.validate_on_submit():
        product_name = Product.query.filter_by(pro_name=form.pro_name.data).first()
        if product_name is None:
            product = Product(pro_name=form.pro_name.data, person=form.person.data)
            db.session.add(product)
            db.session.commit()
            # return redirect(url_for('main.index'))

        else:
            flash('hava exic')
    return render_template('t-addpro.html', form=form)

@main.route('/t-addpackage.html', methods=['GET', 'POST'])
def taddpack():
    form = AddPackage()
    if form.validate_on_submit():
        package_exist = Product_sub.query.filter_by(package=form.package.data, product_id=form.pro_id.data,
                                                    data_Date=form.data_Date.data).first()
        if package_exist is None:
            package = Product_sub(product_id=form.pro_id.data, package=form.package.data, data_Date=form.data_Date.data,
                                  last_time=datetime.now(), data=form.data.data)
            db.session.add(package)
            db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('t-addpackage.html', form=form)

@main.route('/t-addpackage.html', methods=['GET', 'POST'])
def search():
    form = SearchView()
    if form.validate_on_submit():
        'select PS.package 包号,P.pro_name 产品名称,P.person 对接人,PS.last_time 修改时间 from product_sub AS PS LEFT JOIN product AS P on P.id = PS.product_id'

