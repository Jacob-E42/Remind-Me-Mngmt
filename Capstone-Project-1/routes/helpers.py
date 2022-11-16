from app import app
from functools import wraps
from models import db, User,  Task
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import current_user
from twilio.rest import Client

def admin_required(func):
    @wraps(func)
    def validate_is_admin(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            flash("You must be an admin to access this page", "danger")
            return redirect(url_for('login'), code=303)

        return func(*args, **kwargs)

    return validate_is_admin

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc
























# @app.route("/bind")

# def setup_binding():

#     # Your Account SID from twilio.com/console
#     account_sid = ACCOUNT_SID
#     # Your Auth Token from twilio.com/console
#     auth_token = AUTH_TOKEN

#     client = Client(account_sid, auth_token)

#     binding = client.notify.v1 \
#         .services(SERVICE_SID) \
#         .bindings \
#         .create(
#             identity='00000002',
#             binding_type='sms',
#             address='+12063198779'
#         )

#     return render_template("test.html", display=binding.sid)


# @app.route("/status", methods=['POST'])
# def incoming_sms():
#     message_sid = request.values.get('MessageSid', None)
#     message_status = request.values.get('MessageStatus', None)
#     logging.info('SID: {}, Status: {}'.format(message_sid, message_status))
#     return ('', 204)


# @app.route("/change", methods=["POST", "GET"])
# def change_admin_status():
#     current_user.change_admin()
#     db.session.commit()
#     flash("Admin status changed", "success")
#     return redirect("/")


# class Unique(object):
#     """ validator that checks field uniqueness """
#     def __init__(self, model, field, message=None):
#         self.model = model
#         self.field = field
#         if not message:
#             message = u'this element already exists'
#         self.message = message

#     def __call__(self, form, field):         
#         check = self.model.query.filter(self.field == field.data).first()
#         print("**********************************************check: ", check)
#         if check:
#             raise ValidationError(self.message)