from flask import Flask, request, render_template, redirect, url_for, make_response
from flask_migrate import Migrate
from models import Users, db
import os

# Imports
from routes.token_required import token_required
from routes.login import login_routs
from routes.dashboard import dashboard_routs
from extensions import mail

app = Flask(__name__)
# FLASH MESSAGES KE LIYE YE ZAROORI HAI
app.secret_key = "hardik_super_secret_key_for_flash" 

# Rate limiting
from flask_limiter import Limiter
limiter = Limiter(key_func=lambda: request.remote_addr, app=app)

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('sender_email')
app.config['MAIL_PASSWORD'] = os.getenv('sender_password')
mail.init_app(app)

# DB config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

# ROUTES ----------------------------------------------------

# Redirect root to login
@app.route('/')
def home():
    return redirect(url_for('login'))

# GET and POST dono allow karne padenge HTML form ke liye
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_routs()

# Logout route (Cookie delete karne ke liye)
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie('token', '', expires=0) # Cookie delete
    return resp

@app.route('/dashboard', methods=['GET'])
@token_required
def dashboard(current_user):
    return dashboard_routs(current_user)

# Baaki ke routes hum aage ek ek karke Forms me convert karenge...

if __name__ == '__main__':
    app.run(debug=True)