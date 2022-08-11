"""
"""

from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID, SECRET_KEY
from flask_debugtoolbar import DebugToolbarExtension
import os
from twilio.rest import Client
import requests
from urllib.parse import urlparse, urljoin

# --------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///organizations_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#connects db and creates all tables on the db server
connect_db(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"

USER = current_user
BASE_URL = "https://api.txtlocal.com/send/"


# ------------------------------------------------------------------------------------------

@app.route('/')
def show_homepage():

    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        login_user(USER)
        flash('Logged in successfully.')
        next = request.args.get('next')

        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for('show_homepage'))
    else:
        return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        data = {k:v for k,v in form.data.items() if k != "password" and k != "csrf_token"}
        new_user = User.register(form.password.data, data)
        db.session.add(new_user)
        db.session.commit()
        url = url_for('show_homepage')
        return redirect(url)
    else:
        return render_template("signup.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(f"{url_for('show_homepage')}")


@app.route("/remind", methods=["POST", "GET"])
@login_required
def send_sms():
 
    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token  = AUTH_TOKEN

    client = Client(account_sid, auth_token)
    notification = client.notify.services(SERVICE_SID) \
    .notifications.create(
        # We recommend using a GUID or other anonymized identifier for Identity
        identity='00000002',
        body='Knok-Knok! You have gotten your first test')
    print(notification.sid)
    return render_template("test.html", display=notification.sid)


@app.route("/bind")
@login_required
def setup_binding():
    

    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token  = AUTH_TOKEN

    client = Client(account_sid, auth_token)
    
    binding = client.notify.v1 \
                       .services(SERVICE_SID) \
                       .bindings \
                       .create(
                            identity='00000002',
                            binding_type='sms',
                            address='+12063198779'
                        )

    
    return render_template("test.html", display=binding.sid)

@app.route("/status", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    logging.info('SID: {}, Status: {}'.format(message_sid, message_status))

    return ('', 204)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc