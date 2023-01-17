import flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    next = flask.request.args.get('next')
    return render_template('login.html', next=next)

@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    next = request.form.get('next')

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Неправильный логин или пароль')

        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    if next is not None and next != 'None':
        return redirect(next)
    return redirect(url_for('catalog'))


@auth.route('/signup')
def signup():
    next = flask.request.args.get('next')
    return render_template('signup.html', next=next)


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(name=name).first()
    next = request.form.get('next')

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Пользователь с таким именем уже существует')
        return redirect(url_for('auth.signup'))

    new_user = User(name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)

    if next is not None and next != 'None':
        return redirect(next)
    return redirect(url_for('catalog'))

@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('catalog'))