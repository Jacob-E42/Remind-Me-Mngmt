from app import app
from routes.login import admin_required, load_user
from models import db, User, Task, Assignment
from forms import  AssignUserForm,  AssignTaskForm, EditTaskAssignmentForm, EditUserAssignmentForm
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort, jsonify
from flask_login import login_required, current_user


@app.route("/assignments/users/<int:id>", methods=["GET","POST"])
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
        # for task in assigned_task_ids:
        #     if task not in task_choices:
        #         assignment = Assignment.query.filter_by(task_id=task).first()
        #         db.session.delete(assignment)
        #         db.session.commit()
        #         flash("Assignment deleted", "success")
        return redirect(url_for('show_user_details', id=id))
    return render_template("assignments/create_user_assignment.html", form=form, user=user)


@app.route("/assignments/users/<int:user_id>/<int:task_id>", methods=["GET"])
def show_edit_user_assignment(user_id, task_id):
    user = User.query.get_or_404(user_id)
    assignment = Assignment.query.filter_by(assignee_id=user_id, task_id=task_id).first()
    form = EditUserAssignmentForm(obj=assignment)
    form.task_id.choices = [(task.id, task.title) for task in Task.query.all()]
  
    return render_template("assignments/edit_user_assignment.html", form=form, user=user)

@app.route("/assignments/users/<int:user_id>/<int:task_id>", methods=["PUT", "PATCH"])
def edit_user_assignment(user_id, task_id):
    form = EditUserAssignmentForm(obj=request.data)
    assignment = Assignment.query.filter_by(assignee_id=user_id, task_id=task_id).first()
    form.is_submitted()
    if form.validate():
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        for (k, v) in data.items():
            setattr(assignment, k, v)
        db.session.add(assignment)
        db.session.commit()
        flash("Assignment updated!", "success")
        return url_for('show_user', id=user_id)

    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return url_for('show_edit_user_assignment', task_id=task_id, user_id=user_id)


@app.route("/assignments/tasks/<int:id>", methods=["POST"])
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
        # for assignee in assigned_user_ids:
        #     if assignee not in assignee_choices:
        #         assignment = Assignment.query.filter_by(
        #             assignee_id=assignee, task_id=task.id).first()
        #         db.session.delete(assignment)
        #         db.session.commit()
        #         flash("Assignment deleted", "success")
        return redirect(url_for('show_all_tasks'))
    return render_template("assignments/create_user_assignment.html", form=form, task=task)

@app.route("/assignments/tasks/<int:id>", methods=["PUT", "PATCH"])
def edit_task_assignments(id):

    return render_template("assignments/edit_task_assignment.html", form=form, task=task)

@app.route("/assignments/<int:id>", methods=["DELETE"])
@admin_required
def delete_assignment(id):
    task = Task.query.get_or_404(id)
    return "deleted"