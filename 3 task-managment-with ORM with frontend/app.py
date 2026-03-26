from flask import Flask , request, jsonify
from flask_migrate import Migrate
from models import Users , db
import os

# ----------------------------------------------------------------------
from routes.token_required import token_required
from routes.login import login_routs
from routes.admin_create_users import admin_create_users_routs
from routes.manager_create_emp import manager_create_emp
from routes.admin_create_tasks import admin_create_tasks_routs
from routes.manager_create_tasks import manager_create_tasks_routs
from routes.update import update_routs
from routes.delete import delete_routs
from extensions import mail
from routes.dashboard import dashboard_routs

app = Flask(__name__)

# ----------------------------------------------------------------------
# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(key_func=lambda: request.remote_addr, app=app)

# ----------------------------------------------------------------------------------

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('sender_email')
app.config['MAIL_PASSWORD'] = os.getenv('sender_password')

mail.init_app(app) # which app are use
# ----------------------------------------------------------------------



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db.init_app(app) # which app are use
migrate = Migrate(app, db) # make migrate app and db




@app.route('/login', methods = ['POST'])
def login():
    return login_routs()


@app.route('/admin/create-users', methods = ['POST'])
@token_required
def admin_create_user(current_user):
    return admin_create_users_routs(current_user)


@app.route('/manager/create-users', methods = ['POST'])
@token_required
def manager_create_user(current_user):
    return manager_create_emp(current_user)


@app.route('/admin/create-tasks', methods = ['POST'])
@token_required
def admin_create_tasks(current_user):
    return admin_create_tasks_routs(current_user)

@app.route('/manager/create-tasks', methods = ['POST'])
@token_required
def manager_create_tasks(current_user):
    return manager_create_tasks_routs(current_user)


@app.route('/update', methods = ['POST'])
@limiter.limit("5 per minute")
@token_required
def update(current_user):
    return update_routs(current_user)


@app.route('/delete', methods = ['POST'])
@token_required
def delete(current_user):
    return delete_routs(current_user)



@app.route('/dashboard', methods = ['GET'])
@token_required
def dashboard(current_user):
    return dashboard_routs(current_user)

if __name__ == '__main__':
    app.run(debug=True)