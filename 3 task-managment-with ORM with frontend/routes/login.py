from werkzeug.security import check_password_hash
from flask import request, jsonify
import datetime
import jwt
import os
from models import Users

def login_routs():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "email, password are required"}), 400


    try:
        # 1 find user using email
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

            return jsonify({'message': 'Login successful', 'role': user.role, 'token': token}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    
    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500