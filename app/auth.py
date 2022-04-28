from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .models import User, Todo
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Login successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Wrong credentials.', category='error')
        else:
            flash('Email does not exist. Try signing up first', category='error')

    return render_template('login.html', user=current_user)


@auth.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')

        if len(username) < 3:
            flash('Username should be atleast 3 characters', category='error')

        elif len(password) < 8:
            flash("Your password is less than 8 characters", category='error')

        elif password != password2:
            flash('Passwords do not match', category='error')

        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='SHA256'))

            user_exist_check = User.query.filter_by(email=email).first()

            if user_exist_check:
                flash('Email is already in use. Try loggin in', category='error')
            else:
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully. You can now login', category='success')
                return redirect(url_for('auth.login'))

    return render_template('signup.html', user=current_user)
