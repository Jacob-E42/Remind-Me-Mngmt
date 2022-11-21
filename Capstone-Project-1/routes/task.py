from app import app
from routes.login import admin_required, login_required
from routes.helpers import get_users_incomplete_tasks, is_past_due
from models import db, Task, Assignment, User
from forms import CreateTaskForm, EditTaskForm, AssignTaskForm, AssignUserForm
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort, jsonify
from flask_login import current_user



# ------------------------------------------------------------------------------------------------ Task routes

@app.route("/tasks", methods=["GET"])
@admin_required
def show_all_tasks():
    tasks = Task.query.order_by(Task.due_time).all()
    task_ids = [task.id for task in tasks]
    assignments = [assignment for assignment in Assignment.query.all() if assignment.task_id in task_ids]
    return render_template("tasks/all_tasks.html", tasks=tasks, assignments=assignments)

@app.route("/tasks/create", methods=["GET"])
@admin_required
def show_create_task_form():
    form = CreateTaskForm()
    return render_template("tasks/create_task.html", form=form)

@app.route("/tasks", methods=["POST"])
@admin_required
def create_task():
    form = CreateTaskForm(obj=request.data)
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        new_task = Task(created_by=current_user.id, **data)
        db.session.add(new_task)
        db.session.commit()
        flash("New Task Created!", "success")
        return redirect(url_for('show_all_tasks'))
    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return redirect(url_for('show_create_task_form'), code=303)
    

@app.route("/tasks/<int:id>", methods=["GET"])
@login_required
def show_task(id):
    task = Task.query.get_or_404(id)
    assignments = task.assignments
    return render_template("tasks/task_details.html", task=task, assignments=assignments)


@app.route("/tasks/<int:id>/update", methods=["GET"])
@login_required
def show_edit_task_form(id):
    task = Task.query.get_or_404(id)
    form = form = EditTaskForm(obj=task)
    return render_template("tasks/edit_task.html", form=form, task=task)


@app.route("/tasks/<int:id>", methods=["PUT", "PATCH"])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = EditTaskForm(obj=request.data)
    print(form.due_time.data)
    form.is_submitted()
    if form.validate():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        
        for (k, v) in data.items():
            setattr(task, k, v)
        db.session.add(task)
        db.session.commit()
        flash("Task updated!", "success")
        return url_for('show_task', id=id)

    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return url_for('show_edit_task_form', id=id)


@app.route("/tasks/<int:id>", methods=["DELETE"])
@admin_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted!", "danger")
    return url_for('show_all_tasks')

# make accessable only if the task is assigned
@app.route("/tasks/<int:id>/completed", methods=["POST"])
@login_required
def edit_completed_status(id):
    task = Task.query.get_or_404(id)
    task.is_completed = not task.is_completed
    db.session.add(task)
    db.session.commit()
    flash("Completion status changed", "success")
    return task.serialize()


@app.route("/tasks/<int:user_id>/completed", methods=["GET"])
def show_completed_tasks(user_id):
    """returns array of serialized JSON object representations of all completed tasks"""
    
    completed_tasks = get_users_completed_tasks(user_id)
    return jsonify(completed_tasks)
