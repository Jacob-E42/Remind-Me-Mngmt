from flask import Flask, request, redirect, render_template, session, flash, url_for
from models import db, User, Task, Assignment, bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, FlaskLoginClient, AnonymousUserMixin
from sqlalchemy import exc
from datetime import datetime

import os
from unittest import TestCase
from sqlalchemy import exc

os.environ['DATABASE_URL'] = "postgresql:///organizations_test"
from app import app
app.test_client_class = FlaskLoginClient
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///organizations_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SERVER_NAME'] = 'projects'



class UserModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        db.drop_all()
        db.create_all() 
        
        john = User(first_name="John", last_name="Test", username="myself", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="johntest@email.com", phone="5162347644", is_admin=True)
        emily = User(first_name="Emily", last_name="Test", username="myselfish", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="emilytest@email.com", phone="5162347645")
        frank = User(first_name="Frank", last_name="Test", username="myselfy", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="franktest@email.com", phone="5162347646")

        john.id = 1
        emily.id=2
        frank.id = 3


        db.session.add_all([john, emily, frank])
        db.session.commit()

        task1 = Task(resp_type="personal", title="Check Inventory", description="perform weekly inventory count", due_time=datetime(2022, 8, 15), created_by=1)
        task2 = Task(resp_type="personal", title="Make Budget", due_time=datetime(2022, 8, 15), created_by=1)
        task3 = Task(resp_type="personal", title="Reconcile Bank Statements", due_time=datetime(2022, 8, 15), created_by=1)

        task1.id = 1
        task2.id = 2
        task3.id = 3

        db.session.add_all([task1, task2, task3])
        db.session.commit()


    def setUp(self):
        a = User.query.get(1)
        l = User.query.get(2)
        u = AnonymousUserMixin()
        self.u = app.test_client(user=u)
        self.l = app.test_client(user=l)
        self.a = app.test_client(user=a)
        
        
       
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    # def test_get_homepage(self):
    
    #     resp = self.l.get("/")
    #     html = resp.get_data(as_text=True)
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertIn('Home', html)

    def test_login_required_rote(self):
        with app.app_context():
            resp2 = self.l.get(f"{url_for('show_all_users')}")
            resp3 = self.a.get(f"{url_for('show_all_users')}")
            resp1 = self.u.get(f"{url_for('show_all_users')}")
            print(resp1.history)
            html = resp1.get_data(as_text=True)
            self.assertEqual(resp1.status_code, 200)
            self.assertIn("Username", html)
            self.assertEqual(resp2.status_code, 200)
            self.assertIn("All Users", resp2.text)
            self.assertEqual(resp3.status_code, 200)
            self.assertIn("All Users", resp3.text)