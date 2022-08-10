"""
"""

from flask import Flask, request, redirect, render_template, session, flash
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm
from secret import API_SECRET_KEY, ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN
from flask_debugtoolbar import DebugToolbarExtension
import requests




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
 
    return "hooray"


@app.route("/bind")
def setup_binding():
    import os
    from twilio.rest import Client

    # To set up environmental variables, see http://twil.io/secure
    
    

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    binding = client.notify.services('ISXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX') \
        .bindings.create(
            # We recommend using a GUID or other anonymized identifier for Identity
            identity='00000001',
            binding_type='sms',
            address='+15164506401')
    print(binding.sid)
    return "You did it"

@app.route("/status", methods=["GET", "POST", "OPTIONS"])
def receive_status():
    status = request.args
    return jsonify(status)