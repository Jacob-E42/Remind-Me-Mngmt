from flask_wtf import FlaskForm
# from wtforms_alchemy import model_form_factory
from wtforms import StringField, FloatField, PasswordField, EmailField
from models import User, Task, Assignment, db

# BaseModelForm = model_form_factory(FlaskForm)

# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session

# class UserForm(ModelForm):
#     """Form for new user"""
#     class Meta:
#       model = User

# class TaskForm(ModelForm):
#     """Form for a new task"""
#     class Meta:
#       model = Task

class LoginForm(FlaskForm):

  username = StringField("Username")
  password = PasswordField("Password")

class SignupForm(FlaskForm):

  first_name = StringField("First Name")
  last_name = StringField("Last Name")
  username = StringField("Username")
  pasword = PasswordField("Password")
  email = EmailField("Email")
  phone = StringField("Phone Number")
    


# {{ form.hidden_tag() }} <!--add type=hidden form fields -->

#   {% for field in form
#          if field.widget.input_type != 'hidden' %}

#     <p>
#       {{ field.label }}
#       {{ field }}

#       {% for error in field.errors %}
#         {{ error }}
#       {% endfor %}
#     </p>

#   {% endfor %}

#   <button type="submit">Submit</button>