from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

db = SQLAlchemy()


class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36),unique=True,nullable=False,default=lambda: str(uuid.uuid4()))
    role = db.Column(db.Enum('admin', 'manager', 'employee'),nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    # 🔥 self-relation
    creator = db.relationship(
        'Users',
        remote_side=[id],
        backref='created_users'
    )

class Tasks(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36),nullable=False,unique=True,default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'in progress', 'completed'),default='pending',nullable=False)
    assigned_to = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    assigned_by = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)


    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    # relationships
    assignee = db.relationship('Users',foreign_keys=[assigned_to],backref='assigned_tasks')
    assigner = db.relationship('Users',foreign_keys=[assigned_by],backref='created_tasks')


    def dashboard(self):
        return {
            "uuid": self.uuid,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "assigned_to": self.assigned_to,
            "assigned_by": self.assigned_by,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }