""""""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_bcrypt import Bcrypt
from flask_login import UserMixin


bcrypt = Bcrypt()

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model, UserMixin):
     
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email  = db.Column(db.Text, nullable=False, unique=True)
    phone = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    assignments = db.relationship("Assignment", back_populates="user", cascade="all, delete-orphan")
    tasks = db.relationship("Task", viewonly=True, secondary="assignments", back_populates="users")

    def __repr__(self):
        
        return f"{self.first_name} {self.last_name} - {self.id}"
   
    def change_admin(self):
        self.is_admin = not self.is_admin

    def serialize(self):

        return {"id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "username": self.username,
        "password": self.password,
        "email": self.email,
        "phone": self.phone,
        "created_at": self.created_at,
        "is_admin": self.is_admin}
    
    def change_password(self, pwd):
        hashed = bcrypt.generate_password_hash(pwd, rounds=14)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        self.password = hashed_utf8

    def authenticate_password(self, pwd):
        if bcrypt.check_password_hash(self.password, pwd):
            # return user instance
            return True
        else:
            return False

    @classmethod
    def register(cls, pwd, data):
        hashed = bcrypt.generate_password_hash(pwd, rounds=14)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        new_user = cls(password=hashed_utf8, **data)
        if new_user:
            return new_user
        else:
            return False

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        u = cls.query.filter_by(username=username).first()
        if not u:
            return (False, "That is not a valid username")
        if u.authenticate_password(pwd):
            # return user instance
            return (u, "Logged in successfully.")
        else:
            return (False, "The password provided is incorrect")


    
class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement='ignore_fk')
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    resp_type = db.Column(db.String(), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    description = db.Column(db.Text)
    due_time  = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL") )
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    time_completed = db.Column(db.DateTime, server_onupdate=db.func.now())

    assignments = db.relationship("Assignment", back_populates="task", cascade="all, delete-orphan")
    users = db.relationship("User", viewonly=True, secondary="assignments", back_populates="tasks")

    def __repr__(self):
        return f" {self.id} {self.title} {self.due_time} {self.is_completed}"

    def serialize(self):

        return {"id": self.id,
        "is_completed ": self.is_completed,
        "resp_type": self.resp_type,
        "title": self.title,
        "description": self.description,
        "due_time": self.due_time,
        "created_by": self.created_by,
        "created_at": self.created_at,
        "time_completed": self.time_completed}

class Assignment(db.Model):

    __tablename__ = "assignments"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assigner_id = db.Column(db.Integer, nullable=False)
    assignee_id = db.Column(db.Integer,  db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"),  nullable=False)
    remind_daily = db.Column(db.Boolean,  default=False)
    notify_admin = db.Column(db.Boolean,  default=False)

 
    task = db.relationship("Task", back_populates="assignments")
    user = db.relationship("User", back_populates="assignments")
    
    def __repr__(self):
        return f" User: {self.assignee_id} Task: {self.task_id} {self.remind_daily} {self.notify_admin} "
    
    def serialize(self):

        return {"id": self.id,
        "assigner_id": self.assigner_id,
        "assignee_id": self.assignee_id,
        "task_id": self.task_id,
        "remind_daily": self.remind_daily,
        "notify_admin": self.notify_admin}

