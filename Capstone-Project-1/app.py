"""
"""

from models import db, connect_db
from secret import SECRET_KEY
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import current_user
from flask_debugtoolbar import DebugToolbarExtension
import requests
from twilio.rest import Client
import os


# -------------------------------------------------------------------------------- Setup and Configurations

app = Flask(__name__)

from routes import helpers, login, user,  task,  reminder, assignment

uri = os.environ.get("DATABASE_URL", 'postgresql:///organizations_db')  
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['DEBUG'] = True

debug = DebugToolbarExtension(app)

# connects db and creates all tables on the db server
connect_db(app)
db.create_all()




@app.route('/')
def show_homepage():
    if (current_user.is_authenticated):
        if (current_user.is_admin):
             return render_template("/homepages/admin_user_home.html")
        else:
            return render_template("/homepages/regular_user_home.html")
    return render_template("/homepages/anon_user_home.html")
   