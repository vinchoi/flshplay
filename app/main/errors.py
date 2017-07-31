from flask import render_template
from . import main
from flask_login import login_required

@main.app_errorhandler(404)
@login_required
def page_of_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
@login_required
def page_of_found(e):
    return render_template('500.html'), 500