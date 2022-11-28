import os


from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, FlaskLoginClient, UserMixin
from sqlalchemy import exc, func
from datetime import datetime


from unittest import TestCase


os.environ['DATABASE_URL'] = "postgresql:///organizations_test"
from app import app
from models import db, User, Task, Assignment, bcrypt
app.test_client_class = FlaskLoginClient
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///organizations_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']






class UserModelTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        db.session.rollback()
        # db.drop_all()
        # db.create_all() 
        User.query.delete()
        
        # john = User(first_name="John", last_name="Test", username="myself", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="johntest@email.com", phone="5162347644", is_admin=True)
        emily = User(first_name="Emily", last_name="Test", username="myselfish", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="emilytest@email.com", phone="5162347645")
        # frank = User(first_name="Frank", last_name="Test", username="myselfy", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="franktest@email.com", phone="5162347646")

        # john.id = 1
        emily.id=2
        # frank.id = 3


        db.session.add_all([ emily])
        db.session.commit()


    def setUp(self):
      
        u = User.query.get(2)
        self.u = u
       
    def tearDown(self):
  
        result = super().tearDown()
        db.session.rollback()
        return result
        
    def test_user_model(self):
        user = User(id=5, first_name="Ted", last_name="Test", username="myselfddish22", password="testPaswd11", email="emilyt@email.com2", phone="5162347647")
        db.session.add(user)
        db.session.commit()
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.is_anonymous)
        self.assertTrue(user.id)
        self.assertTrue(user.first_name)
        self.assertTrue(user.last_name)
        self.assertTrue(user.username)
        self.assertTrue(user.password)
        self.assertTrue(user.email)
        self.assertTrue(user.phone)
        self.assertTrue(user.created_at)
        self.assertIsInstance(user.assignments, list)
        self.assertIsInstance(user.tasks, list)
       

class UserREgistrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
       
        # db.drop_all()
        # db.create_all() 
        User.query.delete()
        db.session.rollback()
        # john = User(first_name="John", last_name="Test", username="myself", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="johntest@email.com", phone="5162347644", is_admin=True)
        emily = User(first_name="Emily", last_name="Test", username="myselfish", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="emilytest@email.com", phone="5162347645")
        # frank = User(first_name="Frank", last_name="Test", username="myselfy", password=bcrypt.generate_password_hash("password", rounds=14).decode("utf8"), email="franktest@email.com", phone="5162347646")

        # john.id = 1
        emily.id=2
        # frank.id = 3


        db.session.add_all([ emily])
        db.session.commit()


    def setUp(self):
      
        u = User.query.get(2)
        self.u = u
       
    def tearDown(self):
  
        result = super().tearDown()
        db.session.rollback()
        return result

    # def test_valid_registration(self):
    #     data = {"first_name":'ted', "last_name":"Teddy", "username":"Tedster", "email":"ted@email.com", "phone":"1234446789"}
    #     new_user = User.register("bananas", data)
    #     self.assertTrue(new_user)
    #     self.assertEqual(new_user.first_name, "ted")
    #     self.assertEqual(new_user.last_name, "Teddy")
    #     self.assertEqual(new_user.username, "Tedster")
    #     self.assertEqual(new_user.email, "ted@email.com")
    #     self.assertTrue(new_user.password.startswith("$2b$"))
    #     self.assertGreater(len(new_user.password), 12)
    #     self.assertEqual(new_user.is_admin, False)

    def test_invalid_registration(self):
        data = {"last_name":"Teddy", "username":"Tedster", "email":"ted@email.com", "phone":"1234446789"}
        user1 = User.register("bananas", data)
        db.session.add(user1)

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    # def test_valid_authentication(self):
    #     (u,msg) = User.authenticate(self.u.username, "password")
    #     self.assertIsNotNone(u)
    #     self.assertTrue(u)
    #     self.assertEqual(u.id, self.u.id)

    #     u = User.query.filter_by(username=self.u.username).first()
    #     self.assertIsNotNone(u)
    #     self.assertEqual(u.id, 2)
    #     self.assertTrue(u.password.startswith("$2b$"))
    
    # def test_invalid_username(self):
    #     (res, msg) = User.authenticate("badusername", "password")
    #     self.assertFalse(res)

    # def test_wrong_password(self):
    #     (res, msg) = User.authenticate(self.u.username, "badpassword")
    #     self.assertFalse(res)

    # def test_user_serialize(self):
    #     serialized_user = self.u.serialize()
        
    #     self.assertEqual({'id':2, 'first_name': "Emily", 'last_name': "Test",'username':"myselfish", 'email':"emilytest@email.com", 'phone':"5162347645", 'is_admin': False}, {'id': serialized_user['id'], 'first_name': serialized_user['first_name'], 'last_name': serialized_user['last_name'], 'username': serialized_user['username'], 'email':serialized_user['email'] , "phone" : serialized_user['phone'], "is_admin": serialized_user['is_admin']})
