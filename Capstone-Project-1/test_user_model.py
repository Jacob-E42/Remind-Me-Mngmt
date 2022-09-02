from flask import Flask, request, redirect, render_template, session, flash
from models import db, User, Task, Assignment, bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, FlaskLoginClient
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
        u = User.query.get(2)
        
        self.c = app.test_client()
        self.u = u
       
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
        
    def test_user_model(self):
        u = User(first_name="Emily", last_name="Test", username="myselfish22", password="testPwd11", email="emilytest@email.com2", phone="5162347647")
        self.assertFalse(u.is_admin)
        self.assertTrue(u.is_authenticated)
        self.assertFalse(u.is_anonymous)

 

    def test_valid_registration(self):
        data = {"first_name":'ted', "last_name":"Teddy", "username":"Tedster", "email":"ted@email.com", "phone":"1234446789"}
        new_user = User.register("bananas", data)
        self.assertTrue(new_user)
        self.assertEqual(new_user.first_name, "ted")
        self.assertEqual(new_user.username, "Tedster")
        self.assertEqual(new_user.email, "ted@email.com")
        self.assertTrue(new_user.password.startswith("$2b$"))

    def test_invalid_registration(self):
        data = {"last_name":"Teddy", "username":"Tedster", "email":"ted@email.com", "phone":"1234446789"}
        user1 = User.register("bananas", data)
        db.session.add(user1)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_valid_authentication(self):
        (u,msg) = User.authenticate(self.u.username, "password")
        self.assertIsNotNone(u)
        self.assertTrue(u)
        self.assertEqual(u.id, self.u.id)

        u = User.query.filter_by(username=self.u.username).first()
        self.assertIsNotNone(u)
        self.assertEqual(u.id, 2)
        self.assertTrue(u.password.startswith("$2b$"))
    
    def test_invalid_username(self):
        (res, msg) = User.authenticate("badusername", "password")
        self.assertFalse(res)

    def test_wrong_password(self):
        (res, msg) = User.authenticate(self.u.username, "badpassword")
        self.assertFalse(res)

        
   