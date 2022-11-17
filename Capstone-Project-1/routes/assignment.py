from app import app
from routes.login import admin_required, load_user
from routes.helpers import get_assignment
from models import db, User, Task, Assignment
from forms import  AssignUserForm,  AssignTaskForm, EditTaskAssignmentForm, EditUserAssignmentForm
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort, jsonify
from flask_login import login_required, current_user

@app.route("/assignments/users/<int:id>", methods=["GET"])
@login_required
def show_assign_user_form(id):
    user = User.query.get_or_404(id)
    form = AssignUserForm(obj=user)
    assigned_task_ids = [task.id for task in user.tasks]
    form.task_id.choices = [(task.id, task.title) for task in Task.query.all()]
    session["assigned_task_ids"] = assigned_task_ids
    session["choices"] = form.task_id.choices
    return render_template("assignments/create_user_assignment.html", form=form, user=user)

@app.route("/assignments/users/<int:id>", methods=["POST"])
@admin_required
def assign_task_to_user(id):
    form = AssignUserForm(obj=request.data)
    assigned_task_ids = session["assigned_task_ids"]
    form.task_id.choices = session["choices"]

    if form.validate_on_submit():
        form_data = {k: v for k, v in form.data.items() if k !=
                     "csrf_token" and k != "task_id"}
        data = {"assigner_id": current_user.id, "assignee_id": id, **form_data}
        task = form.task_id.data

        
        if (task not in assigned_task_ids) or len(assigned_task_ids) == 0:
            new_assignment = Assignment(task_id=task, **data)
            db.session.add(new_assignment)
            db.session.commit()
            flash("Assignment Created!", "success")
            return redirect(url_for('show_user', id=id))
        # for task in assigned_task_ids:
        #     if task not in task_choices:
        #         assignment = Assignment.query.filter_by(task_id=task).first()
        #         db.session.delete(assignment)
        #         db.session.commit()
        #         flash("Assignment deleted", "success")
        
    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return url_for('show_user_assignment_form', id=id)


@app.route("/assignments/users/<int:user_id>/<int:task_id>", methods=["GET"])
def show_edit_user_assignment(user_id, task_id):
    user = User.query.get_or_404(user_id)
    task = Task.query.get_or_404(task_id)
    form = EditUserAssignmentForm()
    return render_template("assignments/edit_user_assignment.html", form=form, user=user, task=task)

@app.route("/assignments/users/<int:user_id>/<int:task_id>", methods=["PUT", "PATCH"])
@admin_required
def edit_user_assignment(user_id, task_id):
    assignment = get_assignment(user_id, task_id)
    form = EditUserAssignmentForm(obj=request.data)
    form.is_submitted()
    if form.validate():
        assignment.remind_daily = form.remind_daily.data
        assignment.notify_admin = form.notify_admin.data
        db.session.add(assignment)
        db.session.commit()
        flash("Assignment updated!", "success")
        return url_for('show_user', id=user_id)
  
    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return url_for('show_edit_user_assignment', task_id=task_id, user_id=user_id)


@app.route("/assignments/tasks/<int:id>", methods=["GET","POST"])
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
        assignee = form.assignee_id.data

        if (assignee not in assigned_user_ids) or len(assigned_user_ids) == 0:
            new_assignment = Assignment(assignee_id=assignee, **data)
            db.session.add(new_assignment)
            db.session.commit()
            flash("Assignment Created!", "success")
        # for assignee in assigned_user_ids:
        #     if assignee not in assignee_choices:
        #         assignment = Assignment.query.filter_by(
        #             assignee_id=assignee, task_id=task.id).first()
        #         db.session.delete(assignment)
        #         db.session.commit()
        #         flash("Assignment deleted", "success")
        return redirect(url_for('show_all_tasks'))
    return render_template("assignments/create_task_assignment.html", form=form, task=task)

@app.route("/assignments/tasks/<int:task_id>/<int:user_id>", methods=["GET"])
@login_required
def show_edit_task_assignment(task_id, user_id):
    user = User.query.get_or_404(user_id)
    task = Task.query.get_or_404(task_id)
    form = EditTaskAssignmentForm()
    return render_template("assignments/edit_task_assignment.html", form=form, user=user, task=task)

@app.route("/assignments/tasks/<int:task_id>/<int:user_id>", methods=["PUT", "PATCH"])
@admin_required
def edit_task_assignment(task_id, user_id):
    assignment = get_assignment(user_id, task_id)
    form = EditTaskAssignmentForm(obj=request.data)
    form.is_submitted()
    if form.validate():
        assignment.remind_daily = form.remind_daily.data
        assignment.notify_admin = form.notify_admin.data
        db.session.add(assignment)
        db.session.commit()
        flash("Assignment updated!", "success")
        return url_for('show_task', id=task_id)
  
    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return url_for('show_edit_task_assignment', task_id=task_id, user_id=user_id)

@app.route("/assignments/<int:user_id>/<int:task_id>", methods=["DELETE"])
@admin_required
def delete_assignment(user_id, task_id):
    assignment = get_assignment(user_id, task_id)
    db.session.delete(assignment)
    db.session.commit()
    flash("Assignment deleted", "success")
    return {"deleted":"success"}