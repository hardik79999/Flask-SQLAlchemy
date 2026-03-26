from flask import request, redirect, url_for, flash
from functools import wraps
import jwt
import os

def token_required(f):
    @wraps(f)
    def token(*args, **kwargs):
        # Header ki jagah ab hum token COOKIE se nikalenge
        token_string = request.cookies.get('token')

        if not token_string:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login')) # Redirect to login route
        
        try:
            decoded_payload = jwt.decode(token_string, os.getenv('key'), algorithms=["HS256"])

            current_user = {
                "id": decoded_payload.get('id'),
                "uuid": decoded_payload.get('uuid'),
                "role": decoded_payload.get('role'),
                "username": decoded_payload.get('username')
            }

        except jwt.ExpiredSignatureError:
            flash("Token expired! Please login again.", "error")
            return redirect(url_for('login'))
        except jwt.InvalidTokenError:
            flash("Invalid token! Please login again.", "error")
            return redirect(url_for('login'))
        except Exception:
            flash("Something went wrong. Please login again.", "error")
            return redirect(url_for('login'))
        
        return f(current_user, *args, **kwargs)
    return token