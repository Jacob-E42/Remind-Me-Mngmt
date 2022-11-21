from models import db, User, Task, Assignment
from app import app
from datetime import datetime

db.drop_all()
db.create_all()

User.query.delete()
Task.query.delete()
Assignment.query.delete()

john = User.register("testPwd11", {"first_name":"John", "last_name":"Test", "username":"myself",  "email":"johntest@email.com", "phone":"5162347644", "is_admin":True})
emily = User.register("testPwd11", {'first_name':"Emily", "last_name":"Test", "username":"myselfish",  "email":"emilytest@email.com", "phone":"5162347645"})
frank = User.register("testPwd11", {"first_name":"Frank", "last_name":"Test", "username":"myselfy",  "email":"franktest@email.com", "phone":"5162347646"})
jacob = User.register("123456", {"first_name":"Jacob", 'last_name':"Eiferman", "username":"JacobAdmin", "email":"yaakoveiferman@gmail.com", "phone":"5164506401", "is_admin":True})

db.session.add_all([john, emily, frank, jacob])
db.session.commit()

task1 = Task(resp_type="personal", title="Check Inventory", description="perform weekly inventory count", due_time=datetime(2022, 12, 14), created_by=1)
task2 = Task(resp_type="personal", title="Make Budget", due_time=datetime(2022, 12, 16), created_by=1)
task3 = Task(resp_type="personal", title="Reconcile Bank Statements", due_time=datetime(2022, 12, 15), created_by=1)

db.session.add_all([task1, task2, task3])
db.session.commit()

assign1 = Assignment(assigner_id=john.id, assignee_id=john.id, task_id=task1.id)
assign2 = Assignment(assigner_id=john.id, assignee_id=emily.id, task_id=task2.id)
assign3 = Assignment(assigner_id=john.id, assignee_id=frank.id, task_id=task3.id)
assign4 = Assignment(assigner_id=john.id, assignee_id=emily.id, task_id=task3.id)
assign5 = Assignment(assigner_id=jacob.id, assignee_id=jacob.id, task_id=task1.id, notify_admin=True, remind_daily=True)
assign6 = Assignment(assigner_id=jacob.id, assignee_id=jacob.id, task_id=task2.id, notify_admin=True, remind_daily=True)
assign7 = Assignment(assigner_id=jacob.id, assignee_id=jacob.id, task_id=task3.id, notify_admin=True, remind_daily=True)
db.session.add_all([assign1, assign2, assign3, assign4, assign5, assign6, assign7])
db.session.commit()


