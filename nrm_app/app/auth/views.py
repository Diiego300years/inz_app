from flask import render_template, redirect, url_for, request, flash
from . import auth
from flask_login import login_required, current_user, login_user, logout_user
from .forms import LoginForm
from app.models.admin import AdminModel

@auth.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("auth/login.html")


@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        my_user = AdminModel.query.filter_by(email=form.email.data).first()

        if my_user is not None and my_user.check_password(form.password.data):
            login_user(my_user)
            go_next = request.args.get('next')

            if go_next is None or not go_next.startswith('/'):
                go_next = url_for('main.index')
            return redirect(go_next)

        flash('Invalid email or password.', 'warning')

    return render_template('auth/login.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))

@login_required
@auth.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('auth.login'))


