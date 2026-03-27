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

    # self-relation
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



    @staticmethod
    def dashboard(current_user):
        users_data = []
        tasks_data = []
        stats = {}

        try:

            # ================= ADMIN =================
            if current_user['role'] == 'admin':

                all_users = Users.query.filter(Users.role != 'admin').all()

                for u in all_users:
                    creator_name = u.creator.username if u.creator else 'System'

                    users_data.append({
                        "uuid": u.uuid,
                        "username": u.username,
                        "role": u.role,
                        "creator": creator_name
                    })

                stats['total_employee'] = Users.query.filter_by(role='employee').count()
                stats['total_manager'] = Users.query.filter_by(role='manager').count()

                tasks = Tasks.query.filter_by(is_active=True).all()

                for t in tasks:
                    tasks_data.append({
                        "uuid": t.uuid,
                        "title": t.title,
                        "description": t.description,
                        "status": t.status,
                        "assigned_to": t.assignee.username if t.assignee else "Unassigned",
                        "created_at": t.created_at.isoformat(),
                        "updated_at": t.updated_at.isoformat(),
                        "is_my_task": False
                    })

                return {
                    "users": users_data,
                    "tasks": tasks_data,
                    "stats": stats
                }

            # MANAGER ============================================================================================================

            elif current_user['role'] == 'manager':

                stats['total_employee'] = Users.query.filter_by(created_by=current_user['id']).count()

                tasks = Tasks.query.filter_by(assigned_by=current_user['id'],is_active=True).all()

                for t in tasks:
                    tasks_data.append({
                        "uuid": t.uuid,
                        "title": t.title,
                        "description": t.description,
                        "status": t.status,
                        "assigned_to": t.assignee.username if t.assignee else "N/A",
                        "created_at": t.created_at.isoformat(),
                        "updated_at": t.updated_at.isoformat(),
                        "is_my_task": True
                    })

                return {
                    "tasks": tasks_data,
                    "stats": stats
                }

            # EMPLOYEE ============================================================================================================

            elif current_user['role'] == 'employee':

                tasks = Tasks.query.filter_by(assigned_to=current_user['id'],is_active=True).all()

                for t in tasks:
                    tasks_data.append({
                        "uuid": t.uuid,
                        "title": t.title,
                        "description": t.description,
                        "status": t.status,
                        "created_at": t.created_at.isoformat(),
                        "updated_at": t.updated_at.isoformat(),
                        "is_my_task": True
                    })

                return {
                    "tasks": tasks_data
                }

        except Exception as e:
            return {"error": str(e)}