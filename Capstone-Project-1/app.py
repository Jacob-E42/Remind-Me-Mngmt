"""
"""

from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm, CreateTaskForm, EditUserForm, EditTaskForm, AssignUserForm, AssignTaskForm
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from functools import wraps
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID, SECRET_KEY
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta
import requests
from urllib.parse import urlparse, urljoin
import os
from twilio.rest import Client

# -------------------------------------------------------------------------------- Setup and Configurations

app = Flask(__name__)
uri = os.environ.get("DATABASE_URL", 'postgresql:///organizaions_db')  
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# connects db and creates all tables on the db server
connect_db(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "danger"
login_manager.refresh_view = "login"
login_manager.needs_refresh_message = (
    u"To protect your account, please re-login to access this page."
)
login_manager.needs_refresh_message_category = "danger"





# ------------------------------------------------------------------------------------------ User login functions


def admin_required(func):
    @wraps(func)
    def validate_is_admin(*args, **kwargs):
        if not (current_user.is_authenticated and current_user.is_admin):
            flash("You must be an admin to access this page", "danger")
            return redirect(url_for('login'))

        return func(*args, **kwargs)

    return validate_is_admin


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user:
        return user
    return None


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc



# ------------------------------------------------------------------------------------------------- User Routes


@app.route("/users", methods=["GET"])
@login_required
def show_all_users():
    all_users = User.query.all()

    return render_template("users/all_users.html", users=all_users, current_user=current_user)


@app.route("/users/<int:id>", methods=["GET"])
@admin_required
def show_user_details(id):
    user = User.query.get_or_404(id)
    tasks = user.tasks

    return render_template("users/user_details.html", user=user, tasks=tasks)


@app.route("/users/my_tasks", methods=["GET"])
@login_required
def show_all_user_tasks():
    user = User.query.get(4)
    tasks = user.tasks

    return render_template("users/all_user_tasks.html", user=user, tasks=tasks)


# @app.route("/users/<int:id>", methods=["POST"])
# def create_user(id):
#     return "You didn't implement me yet!"


@app.route("/users/<int:id>/edit", methods=["GET", "POST", "PUT", "PATCH"])
@admin_required
def edit_user(id):
    user = load_user(id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        for (k, v) in data.items():
            setattr(user, k, v)
        db.session.add(user)
        db.session.commit()
        flash("User updated!", "success")
        return redirect(url_for('show_user_details', id=user.id))

    return render_template("users/edit_user.html", form=form, user=user)


@app.route("/users/<int:id>", methods=["POST", "DELETE"])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted!", "danger")
    return redirect(url_for('show_all_users'))


@app.route("/users/<int:id>/assign", methods=["GET", "POST"])
@admin_required
def assign_task_to_user(id):
    form = AssignTaskForm()
    user = User.query.get(id)
    assigned_task_ids = [task.id for task in user.tasks]
    form.task_id.choices = [(task.id, task.title) for task in Task.query.all()]

    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k !=
                     "csrf_token" and k != "task_id"}
        data = {"assigner_id": current_user.id, "assignee_id": id, **form_data}
        task_choices = form.task_id.data

        for task in task_choices:
            if (task in task_choices and task not in assigned_task_ids) or len(assigned_task_ids) == 0:
                new_assignment = Assignment(task_id=task, **data)
                db.session.add(new_assignment)
                db.session.commit()
                flash("Assignment Created!", "success")
        for task in assigned_task_ids:
            if task not in task_choices:
                assignment = Assignment.query.filter_by(task_id=task).first()
                db.session.delete(assignment)
                db.session.commit()
                flash("Assignment deleted", "success")
        return redirect(url_for('show_all_tasks'))
    return render_template("users/create_assignment.html", form=form, user=user)
# ------------------------------------------------------------------------------------------------ Task routes


@app.route("/create_task", methods=["GET", "POST"])
@admin_required
def create_task():
    form = CreateTaskForm()
    if form.validate_on_submit():

        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_task = Task(created_by=current_user.id, **data)
        db.session.add(new_task)
        db.session.commit()


        flash("New Task Created!", "success")
        return redirect("/")
    return render_template("tasks/create_task.html", form=form)


@app.route("/tasks", methods=["GET"])
@admin_required
def show_all_tasks():
    tasks = Task.query.order_by(Task.id).all()
    assignments = Assignment.query.all()
    return render_template("tasks/all_tasks.html", tasks=tasks, assignments=assignments)


@app.route("/tasks/<int:id>", methods=["GET"])
def show_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>", methods=["POST"])
def post_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>", methods=["PUT", "PATCH"])
@admin_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = EditTaskForm(obj=task)
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>/delete", methods=["POST", "DELETE"])
@admin_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "danger")
    return redirect(url_for('show_all_tasks'))


@app.route("/tasks/<int:id>/completed", methods=["POST", "PUT", "PATCH"])
@admin_required
def edit_completed_status(id):
    task = Task.query.get_or_404(id)
    task.is_completed = not task.is_completed
    db.session.add(task)
    db.session.commit()
    flash("Status changed", "success")
    return redirect(url_for('show_all_tasks'))


@app.route("/tasks/<int:id>/assignments", methods=["PUT", "PATCH"])
def edit_assignment(id):

    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>/assign", methods=["GET", "POST"])
@admin_required
def assign_user_to_task(id):
    form = AssignUserForm()
    task = Task.query.get(id)
    assigned_user_ids = [user.id for user in task.users]
    form.assignee_id.choices = [(u.id, u.first_name + " " + u.last_name) for u in User.query.all()]

    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items(
        ) if k != "csrf_token" and k != "assignee_id"}
        data = {"assigner_id": current_user.id, "task_id": id, **form_data}
        assignee_choices = form.assignee_id.data

        for assignee in assignee_choices:
            if (assignee in assignee_choices and assignee not in assigned_user_ids) or len(assigned_user_ids) == 0:
                new_assignment = Assignment(assignee_id=assignee, **data)
                db.session.add(new_assignment)
                db.session.commit()
                flash("Assignment Created!", "success")
        for assignee in assigned_user_ids:
            if assignee not in assignee_choices:
                assignment = Assignment.query.filter_by(
                    assignee_id=assignee, task_id=task.id).first()
                db.session.delete(assignment)
                db.session.commit()
                flash("Assignment deleted", "success")
        return redirect(url_for('show_all_tasks'))
    return render_template("tasks/create_assignment.html", form=form, task=task)


@app.route("/tasks/<int:id>/assign", methods=["DELETE"])
@admin_required
def remove_user_from_task(id):
    task = Task.query.get_or_404(id)
    return "deleted"


@app.route("/tasks/upcoming", methods=["GET"])
def show_upcoming_tasks():
    return "You didn't implement me yet!"


@app.route("/tasks/incomplete", methods=["GET"])
def show_incomplete_tasks():
    return "You didn't implement me yet!"


@app.route("/tasks/completed", methods=["GET"])
def show_completed_tasks():
    return "You didn't implement me yet!"


# @app.route("/assign", methods=["GET", "POST"])
# def assign_task_by_default():
#     user_id = current_user.id
#     assign_task(user_id, 1)
#     return redirect("/")  # (url_for('show_user_details', id=user_id))


# ------------------------------------------------------------------------------------------------------ Reminder routes


@app.route("/remind", methods=["POST", "GET"])
@admin_required
def send_sms():

    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token = AUTH_TOKEN

    client = Client(account_sid, auth_token)
    notification = client.notify.services(SERVICE_SID) \
        .notifications.create(
        # We recommend using a GUID or other anonymized identifier for Identity
        identity='00000002',
        body='Knok-Knok! You have gotten your first test')
    print(notification.sid)
    return render_template("test.html", display=notification.sid)


@app.route("/remind/daily", methods=["POST", "GET"])
@admin_required
def send_daily_reminder():
    return "You didn't implement me yet!"


@app.route("/remind/<task_ids>", methods=["POST", "GET"])
@admin_required
def remind_about_tasks(task_ids):
    return "You didn't implement me yet!"


@app.route("/remind/<user_ids>", methods=["POST", "GET"])
@admin_required
def remind_users(user_ids):
    return "You didn't implement me yet!"


@app.route("/notify/<int:task_id>", methods=["POST", "GET"])
@admin_required
def notify_admin(task_id):
    return "You didn't implement me yet!"


@app.route("/bind")
@admin_required
def setup_binding():

    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token = AUTH_TOKEN

    client = Client(account_sid, auth_token)

    binding = client.notify.v1 \
        .services(SERVICE_SID) \
        .bindings \
        .create(
            identity='00000002',
            binding_type='sms',
            address='+12063198779'
        )

    return render_template("test.html", display=binding.sid)


@app.route("/status", methods=['POST'])
def incoming_sms():
    message_sid = request.values.get('MessageSid', None)
    message_status = request.values.get('MessageStatus', None)
    logging.info('SID: {}, Status: {}'.format(message_sid, message_status))
    return ('', 204)


# ------------------------------------------------------------------------ For debugging, to be deleted later

def assign_task(user_id, task_id):
    user = load_user(user_id)
    task = Task.query.get(task_id)
    
    db.session.add(task)
    db.session.commit()


@app.route("/change", methods=["POST", "GET"])
def change_admin_status():
    current_user.change_admin()
    db.session.commit()
    flash("Admin status changed", "success")
    return redirect("/")
