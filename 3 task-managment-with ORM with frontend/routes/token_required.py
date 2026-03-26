from flask import request , jsonify
from functools import wraps
import jwt
import os

def token_required(f):
    @wraps(f)
    def token(*args, **kwrgs):

        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "message": 'Token is missing or invalid format!'
            }), 401
        
        try:
            token_string = auth_header.split(" ")[1]
            if token_string == "":
                raise IndexError
            
            if not token_string:
                return jsonify({"message": "Token part is missing!"}), 401

        except IndexError:
            return jsonify({"message": "Token part is missing...!"}), 401


        try:
            decoded_payload = jwt.decode(token_string, os.getenv('key'), algorithms=["HS256"])

            current_user = {
                "id": decoded_payload.get('id'),
                "uuid": decoded_payload.get('uuid'),
                "role": decoded_payload.get('role'),
                "username": decoded_payload.get('username')
            }

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401
        except Exception:
            return jsonify({"message":"Something went wrong with the token!"}), 401
        
        return f(current_user, *args, **kwrgs)
    return token
