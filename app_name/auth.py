from functools import wraps

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, abort
)
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .forms import LoginForm, RegisterForm
from .models import User
from . import views


bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email.data
        get_user = User.query.filter_by(email=user_email).first()
        if get_user:
            if check_password_hash(get_user.password, form.password.data):
                login_user(get_user)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password entered, please try again.', category='error')

        else:
            flash('Email does not exist, please try again.', category='error')

    return render_template("login.html", form=form, user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    get_user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if not get_user:
            hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
            user_to_add = User(email=form.email.data, password=hashed_pw,
                               username=form.username.data)
            db.session.add(user_to_add)
            db.session.commit()
            login_user(user_to_add)
            return redirect(url_for('views.home'))
        else:
            flash("You've already signed up with that email, log in instead!", category='error')

    return render_template("register.html", form=form, user=current_user)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
