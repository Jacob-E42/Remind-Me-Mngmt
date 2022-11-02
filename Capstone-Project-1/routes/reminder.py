from app import app
from routes.login import admin_required
from models import db, connect_db, User, Assignment, Task
from forms import LoginForm, SignupForm, CreateTaskForm, EditUserForm, EditTaskForm, AssignUserForm, AssignTaskForm
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID, SECRET_KEY
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, UserMixin
from functools import wraps
from flask_debugtoolbar import DebugToolbarExtension
from datetime import timedelta
import requests
from urllib.parse import urlparse, urljoin
from twilio.rest import Client
import os
# ------------------------------------------------------------------------------------------------------ Reminder routes



@app.route("/remind/daily", methods=["POST", "GET"])
@admin_required
def send_daily_reminder():
    all_users = User.query.all()
    for user in all_users:
        remind_user(user.id)
    return "You just reminded everyone!"


@app.route("/remind/task/<int:task_id>", methods=["POST", "GET"])
@admin_required
def remind_for_task(task_id):
    task = Task.query.get(task_id)
    assigned_users = task.users

    for user in assigned_users:
        body = generate_body(user, "task", task)
        reminder = send_sms(user.phone, body)
    return "You sent a reminder about a task!"


@app.route("/remind/user/<user_id>", methods=["POST", "GET"])
@admin_required
def remind_user(user_id):
    
    user = User.query.get(user_id)
    body = generate_body(user, "user")
    
    reminder = send_sms(user.phone, body)
    
    return "You sent a reminder!"


@app.route("/notify/<int:task_id>", methods=["POST", "GET"])
@admin_required
def notify_admin(task_id):
    task = Task.query.get_or_404(task_id)
    admin= User.query.get_or_404(task.created_by)
    body = generate_body(admin, "notify", task)
    reminder = send_sms(admin.phone, body)
    return "You sent a notification!"



def send_sms(recipient, msg):
    # Your Account SID from twilio.com/console
    account_sid = ACCOUNT_SID
    # Your Auth Token from twilio.com/console
    auth_token  = AUTH_TOKEN

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=f"{recipient}", 
        from_="+15706309413",
        status_callback="https://en3ubmjwpivr1.x.pipedream.net",
        body=f"{msg}")

    return message.sid

def generate_body(user, type, task=None):
    if type == "user":
        msg = f"Hi {user.first_name} {user.last_name}, here are your upcoming tasks:\n"
        user_tasks = user.tasks
        for task in user_tasks:
            string = f"The task {task.title} is due by {task.due_time}\n"
            msg += string
        return msg
    elif type == "task":
        
        msg = f"Hi {user.first_name} {user.last_name}, the task {task.title} is due by {task.due_time}."
        return msg
    elif type == "notify":
        msg = f"Hi {user.first_name} {user.last_name}, \n the task {task.title} has been completed."
        return msg
