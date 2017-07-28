#coding:utf-8

from flask import render_template, flash, redirect, url_for, request
from . import auth
from flask_login import login_required, logout_user, login_user
from .forms import LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('welcome back~~')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'登陆失败!用户名或密码错误,请重新登陆.')

    if form.errors:
        flash(u'登陆失败,请尝试重新登陆.')

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆.')
    return redirect(url_for('auth.login'))
