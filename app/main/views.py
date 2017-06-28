#coding:utf-8

from datetime import datetime
from flask import render_template, session, redirect, url_for, flash
from .forms import AddProduct, AddPackage

from . import main
from .. import db
from ..models import Product_sub, Product


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
            product = Product(pro_name=form.pro_name.data)
            print product
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
        product = Product.query.filter_by(pro_name=form.pro_name.data).first()
        product_id = product.id
        package_exist = Product_sub.query.filter_by(package=form.package.data, product_id=product_id).first()
        if package_exist is None:
            package = Product_sub(product_id=product_id, package=form.package.data, last_time=form.last_time.data)
            db.session.add(package)
            db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('t-addpackage.html', form=form)
