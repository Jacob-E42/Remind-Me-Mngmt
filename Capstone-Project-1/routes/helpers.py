from app import app
from functools import wraps
from models import db, User, Task, Assignment
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import current_user
from twilio.rest import Client
from urllib.parse import urlparse, urljoin
from datetime import datetime


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

def get_assignment(user_id, task_id):
    if user_id and task_id:
        return Assignment.query.filter_by(assignee_id=user_id, task_id=task_id).first()
    return None

def get_user_assignments(user_id):
    if user_id:
        return Assignment.query.filter_by(assignee_id=user_id).all()
    return None

def get_users_completed_tasks(user_id):
    if user_id:
        users_assignments = get_user_assignments(user_id)
        return [assignment.task for assignment in users_assignments if assignment.task.is_completed]
    return None

def get_users_incomplete_tasks(user_id):
    if user_id:
        users_assignments = get_user_assignments(user_id)
        return [assignment.task for assignment in users_assignments if assignment.task.is_completed is False]
    return None

def get_current_time():
    return datetime.now()

def is_past_due(task):
    due_time = task.due_time
    now = datetime.now()
    if due_time < now:
        return True
    elif due_time > now:
        return False
    else: 
        return False

def is_due_today(task):
    due_time = task.due_time
    now = datetime.now()
    return due_time.date() == now.date()

@app.route("/flash", methods=["POST"])
def flash_incoming_message():
    flash(request.json["msg"], "danger")
    return ""

def user_has_no_associated_tasks(user):
    user_created_tasks = Task.query.filter_by(created_by=user.id).all()
    print(user_created_tasks)
    if len(user_created_tasks) > 0:
        print("userhasnoassociatedtasks: " )
        flash("There are tasks that are still associated with this user. Delete those tasks first to delete this user.", "danger")
        return False
    return True























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