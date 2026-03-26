from werkzeug.security import check_password_hash
from flask import request, redirect, url_for, flash, make_response, render_template
import datetime
import jwt
import os
from models import Users

def login_routs():
    # Agar user direct URL se aaya hai, toh usko login page dikhao
    if request.method == 'GET':
        return render_template('login.html')

    # Ab data form se aayega, JSON se nahi
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash("Email and password are required", "error")
        return redirect(url_for('login'))

    try:
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            Payload ={
                "id": user.id,
                "uuid": user.uuid,
                "role": user.role,
                "username": user.username,
                "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
            }

            token = jwt.encode(Payload, os.getenv('key'), algorithm="HS256")

            # JSON bhejne ki jagah Redirect response banayenge aur usme cookie chipkayenge
            resp = make_response(redirect(url_for('dashboard')))
            resp.set_cookie('token', token, httponly=True) # Cookie set ho gayi!
            return resp
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for('login'))
    
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('login'))