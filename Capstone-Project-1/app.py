"""
"""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID
from flask_debugtoolbar import DebugToolbarExtension
import os
from twilio.rest import Client
import requests

Yaakov = "+15164506401"
Yehoshua = "+12063198779"




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///organizations_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'c035f65f01c686cae280cb4fe82803f642c14e5a21afede85f7adf94ca252c7c'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

#connects db and creates all tables on the db server
connect_db(app)
db.create_all()

BASE_URL = "https://api.txtlocal.com/send/"

@app.route('/')
def show_homepage():

    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        return redirect("/")
    else:
        return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    print("***************", request)
    form = SignupForm()

    if form.validate_on_submit():
        new_user = User(form.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('show_homepage'))
    else:
        return render_template("signup.html", form=form)


@app.route("/remind", methods=["POST", "GET"])
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
    return f"{notification.sid}"


@app.route("/bind")
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

    print(binding.sid)
    return "You did it"

@app.route("/status", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    logging.info('SID: {}, Status: {}'.format(message_sid, message_status))

    return ('', 204)
