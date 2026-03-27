from flask import request, jsonify
from models import Tasks, Users, db 


def dashboard_routs(current_user):

    try:
        
        # ADMIN
        if current_user['role'] == "admin":
            
            return jsonify(Tasks.dashboard(current_user))
        
        # MANAGER
        elif current_user['role'] == "manager":
            
            return jsonify(Tasks.dashboard(current_user))

        # EMPLOYEE
        elif current_user['role'] == "employee":
            
            return jsonify(Tasks.dashboard(current_user))
            
        else:
            return jsonify({"message": "only register user view dashboard"})
        
        

    except Exception as e:
        return jsonify({"message": str(e)}), 500