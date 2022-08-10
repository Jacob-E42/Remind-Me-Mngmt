from flask import Flask, request, redirect, render_template, session, flash
from models import db #Fix me!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from unittest import TestCase
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' #Fix me!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()




class FlaskTests(TestCase):

    def setUp(self):
        
        fixme = Fixme()
        db.session.add()
        db.session.commit()
        
        
  
        
       
    def tearDown(self):
        fixme = db.session.query(Fixme).first()
        
        db.session.delete(fixme)
     
        db.session.commit()
       
        db.session.rollback()
        
        

    def test_fix_me(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Fixme', html)
    


