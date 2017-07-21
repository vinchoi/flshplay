#coding:utf-8

from flask import render_template, flash, redirect, url_for
from . import auth
from flask_login import login_required, logout_user

@auth.route('/login')
def login():
    return render_template('auth/login.html')




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'注销')
    return redirect(url_for('auth.login'))