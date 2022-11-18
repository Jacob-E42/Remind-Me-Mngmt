from app import app
from routes.login import admin_required
from models import db, User, Task, Assignment
from flask import Flask, request, redirect, render_template, url_for, flash
from secret import ACCOUNT_SID, TEST_AUTH_TOKEN, AUTH_TOKEN, SERVICE_SID
from twilio.rest import Client

# ------------------------------------------------------------------------------------------------------ Reminder routes



@app.route("/remind/daily", methods=["POST"])
@admin_required
def send_daily_reminder():
    all_users = User.query.all()
    for user in all_users:
        body = generate_body(user, "daily")
        reminder = send_sms(user.phone, body)
        flash("You sent daily reminders!", "success")
    return redirect(url_for('show_all_users'))


@app.route("/remind/task/<int:task_id>", methods=["POST"])
@admin_required
def remind_for_task(task_id):
    task = Task.query.get(task_id)
    assigned_users = task.users

    for user in assigned_users:
        body = generate_body(user, "task", task)
        reminder = send_sms(user.phone, body)
        flash("You sent a reminder about a task!", "successs")
    return redirect(url_for('show_all_tasks'))


@app.route("/remind/user/<user_id>", methods=["POST"])
@admin_required
def remind_user(user_id):
    
    user = User.query.get(user_id)
    body = generate_body(user, "user")
    reminder = send_sms(user.phone, body)
    flash("You sent a reminder!", "success")
    return redirect(url_for('show_user', id=user_id))


@app.route("/notify/<int:task_id>/<int:admin_id>", methods=["POST"])
def notify_admin(task_id, admin_id):
    print(task_id, admin_id)
    task = Task.query.get_or_404(task_id)
    admin= User.query.get_or_404(admin_id)
    body = generate_body(admin, "notify", task)
    reminder = send_sms(admin.phone, body)
    flash("You sent a notification!", "success")
    return redirect(url_for('show_all_tasks'))



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
        is_complete = "complete" if task.is_completed else "incomplete"
        msg = f"Hi {user.first_name} {user.last_name}, \n the task {task.title} is now {is_complete}."
        return msg
    elif type == "daily":
        user_assignments = [assignment for assignment in user.assignments if assignment.remind_daily]
        if len(user_assignments) == 0:
             return ""
        msg = f"Hi {user.first_name} {user.last_name}, here are your upcoming tasks for today:\n"
        
        for assignment in user_assignments:
            string = f"The task {assignment.task.title} is due by {assignment.task.due_time}\n"
            msg += string
        return msg
    else:
        return "That is not a valid type indicator"