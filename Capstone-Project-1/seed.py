from models import db, User, Task, Assignment
from app import app
from datetime import datetime

db.drop_all()
db.create_all()

User.query.delete()
Task.query.delete()
Assignment.query.delete()


john = User(first_name="John", last_name="Test", username="myself", password="testPwd11", email="johntest@email.com", phone="5162347644", is_admin=True)
emily = User(first_name="Emily", last_name="Test", username="myselfish", password="testPwd11", email="emilytest@email.com", phone="5162347645")
frank = User(first_name="Frank", last_name="Test", username="myselfy", password="testPwd11", email="franktest@email.com", phone="5162347646")



db.session.add_all([john, emily, frank])
db.session.commit()

task1 = Task(resp_type="personal", title="Check Inventory", description="perform weekly inventory count", due_time=datetime(2022, 8, 15), created_by=1)
task2 = Task(resp_type="personal", title="Make Budget", due_time=datetime(2022, 8, 15), created_by=1)
task3 = Task(resp_type="personal", title="Reconcile Bank Statements", due_time=datetime(2022, 8, 15), created_by=1)

db.session.add_all([task1, task2, task3])
db.session.commit()



