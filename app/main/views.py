#coding:utf-8

from datetime import datetime, timedelta
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from .forms import AddProduct, AddPackage, SearchForm, SearchPackageForm, DeleteProductForm,\
    DeletePackageForm, EditProduct, EditPackage

from . import main
from .. import db
from ..models import Product_sub, Product
from flask_login import login_required, current_user

@main.route('/', methods=['GET', 'POST'])
def rout():
    return redirect(url_for('auth.login'))


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@main.route('/product-table', methods=['GET', 'POST'])
@login_required
def product_table():
    form = AddProduct()
    form1 = DeleteProductForm()
    form2 = EditProduct()

    if form.validate_on_submit():
        product_name = Product.query.filter_by(pro_name=form.pro_name.data, create_by=current_user.id).first()
        page = 1
        if product_name is None:
            product = Product(pro_name=form.pro_name.data.strip(), person=form.person.data.strip(), create_by=current_user.id)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('main.product_table'))
        else:
            flash(u'产品已存在')
    else:
        page = request.args.get('page', 1, type=int)

    if form.errors:
        flash(u'添加失败')

    if current_user.id != 1:
        result = Product.query.order_by(Product.create_time).filter_by(create_by=current_user.id)
    else:
        result = Product.query.order_by(Product.create_time)

    pagination_search = result.paginate(page, per_page=10, error_out=False)

    pagination = pagination_search
    products = pagination_search.items

    return render_template('product-table.html', form=form, form1=form1, form2=form2, pagination=pagination,
                           page=page, endpoint='main.product_table', products=products)


@main.route('/product-table/get-product-info/<int:id>')
@login_required
def get_product_info(id):
    if request.is_xhr:
        product = Product.query.get_or_404(id)
        return jsonify({
            'pro_name': product.pro_name,
            'person': product.person
        })


@main.route('/product-table/edit-product', methods=['POST'])
@login_required
def edit_product():
    form2 = EditProduct()
    page = request.args.get('page', 1, type=int)
    if form2.validate_on_submit():
        product_id = int(form2.product_id.data)
        create_userid = Product.query.filter_by(id=product_id).first().create_by

        if Product.query.filter_by(pro_name=form2.pro_name.data.strip(), create_by=create_userid).first() \
                and Product.query.filter_by\
                            (pro_name=form2.pro_name.data.strip(), create_by=create_userid).first().id != product_id:

            flash(u'已存在该产品')

        else:
            pro_name = form2.pro_name.data
            person = form2.person.data
            product = Product.query.get_or_404(product_id)
            product.pro_name = pro_name
            product.person = person

            db.session.add(product)
            db.session.commit()
            flash(u'修改成功')
            return redirect(url_for('main.product_table', page=page))
    if form2.errors:
        flash(u'修改失败')
    return redirect(url_for('main.product_table', page=page))


@main.route('/product-table/delete-product', methods=['GET', 'POST'])
@login_required
def delete_product():
    form = DeleteProductForm()

    if form.validate_on_submit():
        product_id = int(form.productId.data)
        product = Product.query.get_or_404(product_id)
        count = product.product_sub.count()
        for package in product.product_sub:
            db.session.delete(package)

        '''delete'''
        db.session.delete(product)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败')
        else:
            flash(u'已删除该产品和%s条数据' % count)
    if form.errors:
        flash(u'删除失败')

    return redirect(url_for('main.product_table'))


@main.route('/package-table', methods=['GET', 'POST'])
@login_required
def packagetable():
    productid_choice = request.args.get('productid_choice', -1, type=int)
    form = AddPackage(userid=current_user.id)
    form1 = SearchPackageForm()
    form2 = DeletePackageForm()
    form3 = EditPackage(userid=current_user.id)

    product_choices = [(product_choice.id, product_choice.pro_name)
                       for product_choice in Product.query.filter_by(create_by=current_user.id)]
    product_choices.append((-1, u'全部产品'))
    form1.product.choices = product_choices  # 筛选时选择

    pagination_search = 0

    if form1.validate_on_submit() or request.args.get('productid_choice') is not None:  # 判断是否查询 或 是否携带产品id

        if form1.validate_on_submit():  # 判断是否查询
            productid_choice = form1.product.data  # 根据产品ID查询产品的数据
            page = 1
            result = Product_sub.query.order_by(Product_sub.product_id, Product_sub.package)  # 先总查询

        elif request.args.get('productid_choice') != u'-1':
            productid_choice = request.args.get('productid_choice', type=int)  # 查询产品
            form1.product.data = productid_choice
            page = request.args.get('page', 1, type=int)
            result = Product_sub.query.order_by(Product_sub.product_id, Product_sub.package)  # 先总查询

        else:
            productid_choice = request.args.get('productid_choice', type=int)  # 查询产品
            form1.product.data = productid_choice
            page = request.args.get('page', 1, type=int)
            result = db.session.query(Product_sub).outerjoin(Product, Product_sub.product_id == Product.id).\
                order_by(Product_sub.product_id, Product_sub.package).\
                filter(Product.create_by == current_user.id)

        if productid_choice != -1:  # 非查询全部产品
            product = Product.query.get_or_404(productid_choice)
            result = result.filter_by(product=product)  # 再添加查询条件
        #  制作分页的
        pagination_search = result.paginate(page, per_page=10, error_out=False)
    else:
        form1.product.data = productid_choice  # 赋值筛选栏的默认值

    if pagination_search != 0:  # 判断是否带着查询数据
        pagination = pagination_search
        packages = pagination_search.items

    else:  # 查询全部产品
        page = request.args.get('page', 1, type=int)
        pagination = db.session.query(Product_sub).outerjoin(Product, Product_sub.product_id == Product.id).\
            order_by(Product_sub.product_id, Product_sub.package).\
            filter(Product.create_by == current_user.id).paginate(page, per_page=10, error_out=False)
        packages = pagination.items

    if form.validate_on_submit():  # 判断是否新增数据

        package_exist = Product_sub.query.filter_by(package=form.package.data, product_id=form.pro_id.data,
                                                    data_Date=form.data_Date.data).first()
        if package_exist is None:
            product = Product.query.filter_by(id=form.pro_id.data).first()
            package = Product_sub(product=product, package=form.package.data, data_Date=form.data_Date.data,
                                  last_time=datetime.now(), data=form.data.data)
            db.session.add(package)
            db.session.commit()
            return redirect(url_for('main.packagetable'))

        else:
            flash(u'该产品包号已存当天的数据噜')
    return render_template('package-table.html', packages=packages, pagination=pagination,
                           form=form, form1=form1, form2=form2, form3=form3,
                           page=page, productid_choice=productid_choice, endpoint='main.packagetable')


@main.route('/package-table/get-package-info/<int:id>')
@login_required
def get_package_info(id):
    if request.is_xhr:
        package = Product_sub.query.get_or_404(id)
        return jsonify({
            'product': package.product.id,
            'package': package.package,
            'data': package.data,
            'data_Date': str(package.data_Date)
        })


@main.route('/package-table/edit-package', methods=['POST'])
@login_required
def edit_package():
    form3 = EditPackage()
    page = request.args.get('page', 1, type=int)
    if form3.validate_on_submit():
        package_id = int(form3.package_id.data)

        #  判断条件1:当前产品id and 产品包号 and 该包号当天的数据 是否存在  2.如果存在,是否为当前修改数据 是的话可以修改,不是不可以
        if Product_sub.query.filter_by(product_id=form3.pro_id.data, package=form3.package.data,
                                       data_Date=form3.data_Date.data).first() \
                and Product_sub.query.filter_by(product_id=form3.pro_id.data, package=form3.package.data,
                                       data_Date=form3.data_Date.data).first().id != package_id:
            flash(u'已存在该产品')
        else:
            package_eidt = form3.package.data
            data_edit = form3.data.data
            data_Date_edit = form3.data_Date.data

            package = Product_sub.query.get_or_404(package_id)
            package.package = package_eidt
            package.data = data_edit
            package.data_Date = data_Date_edit

            db.session.add(package)
            db.session.commit()
            flash(u'修改成功')
            return redirect(url_for('main.packagetable', page=page))
    if form3.errors:
        print form3.errors
        flash(u'修改失败')
    return redirect(url_for('main.packagetable', page=page))


@main.route('/package-table/delete-package', methods=['GET', 'POST'])
@login_required
def delete_package():
    form = DeletePackageForm()

    if form.validate_on_submit():
        package_id = int(form.packageId.data)
        package = Product_sub.query.get_or_404(package_id)

        '''delete'''
        db.session.delete(package)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u'删除失败')
        else:
            flash(u'删除成功')
    if form.errors:
        flash(u'删除失败')

    return redirect(url_for('main.packagetable'))


@main.route('/dataview', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    begin_date = form.begin_time.data
    end_date = form.end_time.data

    if begin_date or end_date:

        if begin_date is not None and end_date is None:  # 结束时间为空,查询到后一个月
            end_date = begin_date + timedelta(days=31)

        if begin_date is None and end_date is not None:  # 开始时间为空,查询到前一个月
            begin_date = end_date + timedelta(days=-31)

        result = Product_sub.query.outerjoin(Product, Product_sub.product_id == Product.id).add_entity(Product).\
            order_by(Product.pro_name, Product_sub.package, Product_sub.data_Date)\
            .filter(Product_sub.data_Date.between(begin_date, end_date), Product.create_by == current_user.id)
    else:
        result = Product_sub.query.outerjoin(Product, Product_sub.product_id == Product.id).add_entity(Product).\
            order_by(Product.pro_name, Product_sub.package, Product_sub.data_Date).\
            filter(Product.create_by == current_user.id)

    return render_template('dataview.html', result=result, form=form)

