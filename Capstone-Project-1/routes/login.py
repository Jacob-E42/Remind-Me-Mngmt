from app import app
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm, CreateTaskForm, EditUserForm, EditTaskForm, AssignUserForm, AssignTaskForm
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID, SECRET_KEY
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta
import requests
from urllib.parse import urlparse, urljoin
from twilio.rest import Client
import os
from templates import login, tasks, users


# -------------------------------------------------------------------------------------- User-login Routes
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please re-login to access this page."
)
login_manager.needs_refresh_message_category = "danger"


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        (user, msg) = User.authenticate(form.username.data, form.password.data)
        if user:
            delta = timedelta(days=30)
            login_user(user, remember=True, duration=delta)
            flash(msg, "success")
            next = request.args.get('next')

            # is_safe_url should check if the url is safe for redirects.
            # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('show_homepage'))
        else:
            flash(msg, "danger")

    return render_template("login/login.html", form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items(
        ) if k != "password" and k != "csrf_token"}
        new_user = User.register(form.password.data, data)
        db.session.add(new_user)
        db.session.commit()

        delta = timedelta(days=30)
        login_user(new_user, remember=True, duration=delta)
        flash('Signed up successfully!', "success")
        url = url_for('show_homepage')
        return redirect(url)
    else:
        return render_template("login/signup.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out", "info")
    return redirect(f"{url_for('show_homepage')}")


# ------------------------------------------------------------------------------------------ User login functions


def admin_required(func):
    @wraps(func)
    def validate_is_admin(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            flash("You must be an admin to access this page", "danger")
            return redirect(url_for('login'))

        return func(*args, **kwargs)

    return validate_is_admin


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc