from app import app
from routes.login import admin_required, load_user
from routes.reminder import remind_user
from routes.helpers import user_has_no_associated_tasks, admin_or_own
from models import db, User, Task, Assignment
from forms import  EditUserForm, AssignUserForm, CreateUserForm, AssignTaskForm, ChangePasswordForm
from flask import Flask, request, redirect, render_template, session, flash, url_for, abort, jsonify
from flask_login import login_required, current_user




# ------------------------------------------------------------------------------------------------- User Routes
@app.route("/users", methods=["GET"])
@login_required
def show_all_users():
    all_users = User.query.all()

    return render_template("users/all_users.html", users=all_users, current_user=current_user)


@app.route("/users/<int:id>", methods=["GET"])
@admin_or_own
def show_user(id):
    if id == 0:
        return redirect('login')
    user = User.query.get_or_404(id)
    assignments = user.assignments
    return render_template("users/user_details.html", user=user, assignments=assignments, current_user=current_user)

@app.route("/users/create", methods=["GET"])
@admin_required
def show_create_user_form():
    form = CreateUserForm()
    return render_template("users/create_user.html", form=form)

@app.route("/users", methods=["POST"])
@admin_required
def create_user():
    form = CreateUserForm(obj=request.data)
    if form.validate_on_submit():
        data = {k: v for k, v in form.data.items(
        ) if k != "password" and k != "csrf_token"}
        new_user = User.register(form.password.data or "123456", data)
        db.session.add(new_user)
        db.session.commit()

        flash('Created New User!', "success")
        return redirect(url_for('show_all_users'))
    else:
        return redirect(url_for('show_create_user_form'), code=303)
    
@app.route("/users/<int:id>/update", methods=["GET"])
@login_required
def show_edit_user_form(id):
    user = load_user(id)
    form = EditUserForm(obj=user)
    return render_template("users/edit_user.html", form=form, user=user)

@app.route("/users/<int:id>", methods=["PUT", "PATCH"])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=request.data)
    form.is_submitted()
    if form.validate():
      
        data = {k: v for k, v in form.data.items() if k != "csrf_token"}
        for (k, v) in data.items():
            setattr(user, k, v)
        db.session.add(user)
        db.session.commit()
        flash("User updated!", "success")
        return url_for('show_user', id=id)

    for field in form:
        for error in field.errors:
            flash(error, "danger")
    return url_for('show_edit_user_form', id=id)

    
@app.route("/users/<int:id>", methods=["DELETE"])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if not user_has_no_associated_tasks(user): 
        return jsonify({"error": "delete failed"})
    db.session.delete(user)
    db.session.commit()
    flash("User deleted!", "danger")
    return jsonify(user.serialize())

@app.route("/users/usernames", methods=["GET"])
def get_all_usernames():
    usernames = [user.username for user in User.query.all()]
    return jsonify(usernames)

@app.route("/users/<int:id>/password", methods=["GET"])
@login_required
def get_password_form(id):
    form = ChangePasswordForm()
    user = User.query.get_or_404(id)
    return render_template("/users/change_password_form.html", user=user, form=form)

@app.route("/users/<int:id>/password", methods=["POST"])
@login_required
def change_password(id):
    form = ChangePasswordForm(obj=request.data)
    print(request.data)
    user = User.query.get_or_404(id)
    if form.validate_on_submit():
        if user.authenticate_password(form.previous_password.data):
            user.change_password(form.second_password.data)
            db.session.add(user)
            db.session.commit()
            flash("Password Updated!", "success")
            return redirect(url_for("show_user", id=id))
        else:
            flash("Previous password provided is incorrect.", "danger")

    for field in form:
        for error in field.errors:
            flash(error, "danger")
            print(error)
    return redirect(url_for('get_password_form', id=id))

@app.route("/users/<int:id>/tasks", methods=["GET"])
@login_required
def get_all_my_tasks(id):
    user = User.query.get_or_404(id)
    serialized_tasks = [task.serialize() for task in user.tasks]
    return jsonify(serialized_tasks)

@app.route("/users/change", methods=["POST", "GET"])
def change_admin_status():
    
    current_user.change_admin()
    db.session.commit()
    flash("Admin status changed", "success")
    return redirect(request.referrer)