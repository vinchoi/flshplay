#coding:utf-8

from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, request, jsonify
from .forms import AddProduct, AddPackage, SearchForm, ManagePackageForm, DeleteProductForm,\
    DeletePackageForm, EditProduct, EditPackage

from . import main
from .. import db
from ..models import Product_sub, Product

@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @main.route('/t-addpro.html', methods=['GET', 'POST'])
# def taddpro():
#     form = AddProduct()
#     if form.validate_on_submit():
#         product_name = Product.query.filter_by(pro_name=form.pro_name.data).first()
#         if product_name is None:
#             product = Product(pro_name=form.pro_name.data, person=form.person.data)
#             db.session.add(product)
#             db.session.commit()
#             # return redirect(url_for('main.index'))
#
#         else:
#             flash('hava exic')
#     return render_template('t-addpro.html', form=form)

@main.route('/product-table', methods=['GET', 'POST'])
def product_table():  # taddproduct
    form = AddProduct()
    form1 = DeleteProductForm()
    form2 = EditProduct()

    if form.validate_on_submit():
        product_name = Product.query.filter_by(pro_name=form.pro_name.data).first()
        page = 1
        if product_name is None:
            product = Product(pro_name=form.pro_name.data, person=form.person.data)
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('main.product_table'))
        else:
            flash(u'产品已存在')
    else:
        page = request.args.get('page', 1, type=int)

    if form.errors:
        flash(u'添加失败')

    result = Product.query.order_by(Product.create_time)

    pagination_search = result.paginate(page, per_page=10, error_out=False)

    pagination = pagination_search
    products = pagination_search.items

    return render_template('product-table.html', form=form, form1=form1, form2=form2, pagination=pagination,
                           page=page, endpoint='main.product_table', products=products)

@main.route('/product-table/get-product-info/<int:id>')
def get_product_info(id):
    if request.is_xhr:
        product = Product.query.get_or_404(id)
        return jsonify({
            'pro_name': product.pro_name,
            'person': product.person
        })

@main.route('/product-table/edit-product', methods=['POST'])
def edit_product():
    form2 = EditProduct()
    page = request.args.get('page', 1, type=int)
    if form2.validate_on_submit():
        product_id = int(form2.product_id.data)

        if Product.query.filter_by(pro_name=form2.pro_name.data).first() \
                and Product.query.filter_by(pro_name=form2.pro_name.data).first().id != product_id:

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
def packagetable():
    form = AddPackage()
    form1 = ManagePackageForm()
    form2 = DeletePackageForm()
    form3 = EditPackage()

    product_choices = [(product_choice.id, product_choice.pro_name) for product_choice in Product.query.all()]
    product_choices.append((-1, u'全部产品'))
    form1.product.choices = product_choices
    # form3.pro_id.choices = product_choices

    pagination_search = 0

    if form1.validate_on_submit():  # 判断是否查询
        productid_choice = form1.product.data  # 根据产品ID查询产品的数据
        page = 1
    else:
        productid_choice = request.args.get('product_id', -1, type=int)  # 查询全部产品
        form1.product.data = productid_choice
        page = request.args.get('page', 1, type=int)

    result = Product_sub.query.order_by(Product_sub.product_id, Product_sub.package)  # 先总查询

    if productid_choice != -1:
        product = Product.query.get_or_404(productid_choice)
        result = result.filter_by(product=product)  # 再添加查询条件
    #  制作分页的
        pagination_search = result.paginate(
            page, per_page=10, error_out=False)

    if pagination_search != 0:
        pagination = pagination_search
        packages = pagination_search.items

    else:
        page = request.args.get('page', 1, type=int)
        pagination = Product_sub.query.order_by(Product_sub.product_id, Product_sub.package).paginate(
                page, per_page=10, error_out=False)
        packages = pagination.items

    if form.validate_on_submit():  # 判断是否新增

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
                           page=page, endpoint='main.packagetable')


@main.route('/package-table/get-package-info/<int:id>')
def get_package_info(id):
    if request.is_xhr:
        package = Product_sub.query.get_or_404(id)
        return jsonify({
            'product_name': package.product.pro_name,
            'package': package.package,
            'data': package.data,
            'data_Date': str(package.data_Date)
        })


@main.route('/package-table/edit-package', methods=['POST'])
def edit_package():
    form3 = EditPackage()
    page = request.args.get('page', 1, type=int)
    '''---------'''
    form3.pro_id.choices
    if form3.validate_on_submit():
        package_id = int(form3.package_id.data)
        # package_dataDate = form3.data_Date.data

        if Product_sub.query.filter_by(product_id=form3.pro_id.data, package=form3.package.data,
                                       data_Date=form3.data_Date.data).first() \
                and Product_sub.query.filter_by(product_id=form3.product_id.data, package=form3.package.data,
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


# @main.route('/t-addpackage.html', methods=['GET', 'POST'])
# def taddpack():
#     form = AddPackage()
#     if form.validate_on_submit():
#         package_exist = Product_sub.query.filter_by(package=form.package.data, product_id=form.pro_id.data,
#                                                     data_Date=form.data_Date.data).first()
#         if package_exist is None:
#             product = Product.query.filter_by(id=form.pro_id.data).first()
#             package = Product_sub(product=product, package=form.package.data, data_Date=form.data_Date.data,
#                                   last_time=datetime.now(), data=form.data.data)
#             db.session.add(package)
#             db.session.commit()
#             return redirect(url_for('main.index'))
#
#         else:
#             flash('wodemamayayafdpfkjdsjfisdjifosdjofijsdoifjsfjisj')
#
#     return render_template('t-addpackage.html', form=form)

@main.route('/dataview', methods=['GET', 'POST'])
# @main.route('/t-search.html', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        begin_date = form.begin_time.data
        end_date = form.end_time.data
        result =Product_sub.query.join(Product, Product_sub.product_id == Product.id).add_entity(Product).\
            order_by(Product.pro_name,Product_sub.package).filter(Product_sub.data_Date.between(begin_date, end_date))
    else:
    # sql=Product_sub.query.outerjoin(Product).filter()
        result = Product_sub.query.join(Product, Product_sub.product_id == Product.id).add_entity(Product).\
            order_by(Product.pro_name, Product_sub.package).all()

        # 'select PS.package 包号,P.pro_name 产品名称,P.person 对接人,PS.last_time 修改时间 from product_sub AS PS LEFT JOIN product AS P on P.id = PS.product_id'
    # return render_template('t-search.html', result=result)
    return render_template('dataview.html', result=result, form=form)

# trans_details.query.outerjoin(Uses).filter(Users.username.like('%xx%'))
