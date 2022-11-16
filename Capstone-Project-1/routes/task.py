from app import app
from routes.login import admin_required, login_required
from models import db, Task, Assignment, User
from forms import CreateTaskForm, EditTaskForm, AssignTaskForm, AssignUserForm
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort
from flask_login import current_user



# ------------------------------------------------------------------------------------------------ Task routes


@app.route("/tasks/create", methods=["GET", "POST"])
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
    task = Task.query.get_or_404(id)
    users = task.users
    
    return render_template("tasks/task_details.html", task=task, users=users)


@app.route("/tasks/<int:id>", methods=["POST"])
def post_task(id):
    return "You didn't implement me yet!"


@app.route("/tasks/<int:id>/update")
@login_required
def show_edit_task_form():
    return "You didn't implement me yet"


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


@app.route("/tasks/<int:id>/completed/<int:user>", methods=["POST"])
@login_required
def edit_completed_status(id, user):
    task = Task.query.get_or_404(id)
    task.is_completed = not task.is_completed
    db.session.add(task)
    db.session.commit()
    flash("Status changed", "success")
    return redirect(url_for('notify_admin', task_id=id, user_id=user), code=307)


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