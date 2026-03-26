from flask import request, jsonify
from models import Users, db
from werkzeug.security import generate_password_hash


from flask_mail import Mail , Message
from extensions import mail
import os

def admin_create_users_routs(current_user):


    if current_user['role'] != 'admin':
        return jsonify({"message": "You are not an Admin. Access Denied."}), 403

    data = request.get_json()
    role = data.get('role')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not role or not email or not password:
        return jsonify({"message": "Missing required fields"}), 400
    

    if role not in ['manager', 'employee']:
        return jsonify({"message": "Role must be manager or employee"}), 400
    
    
    try: 
        chack_user = Users.query.filter_by(email=email).first()
        if chack_user:
            return jsonify({"message": "Email already exists"}), 409
        
        hash_password = generate_password_hash(password)

        new_user = Users(role=role, email=email,username=username, password=hash_password, created_by=current_user['id'])
        db.session.add(new_user)
        db.session.commit()

        try:
            msg = Message(
                subject=f"Welcome to Task Management System - Your employee Account",
                sender=os.getenv('sender_email'),
                recipients=[email]
            )

            
            msg.body = f"""Dear {username},

Welcome to the Task Management System!

Your account has been successfully created with the role of '{role}'. Below are your official login credentials:

Email: {email}
Password: {password}

Please log in to the system to access your dashboard and start your work. We highly recommend keeping your credentials secure.

Best Regards,
The Admin Team"""
            
            mail.send(msg)
            print("Email sent successfully to", email)
        except Exception as e:
            print("Failed to send email:", str(e))
            
        return jsonify({
            "send": f"Email sent successfully to{email}",
            "status": True,
            "role": "employee",
            "message": f"Welcome to Task Management System - Your {role} Account"
        }), 200
    
    except Exception as e:
        if db.session:
            db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500
    

            


        