from flask import request, jsonify
from models import Tasks, Users, db 


def dashboard_routs(current_user):

    try:
        
        
        if current_user['role'] == "admin":
            
            return Tasks.admin_dashboard()

        elif current_user['role'] == "manager":
            
            task = Tasks.query.filter_by(assigned_by=current_user['id']).all()

            return jsonify([t.dashboard() for t in task])

        elif current_user['role'] == "employee":
            
            task = Tasks.query.filter_by(assigned_to=current_user['id']).all()

            return jsonify([t.dashboard() for t in task])

        else:
            return jsonify({"message": "only register user view dashboard"})
        
        

    except Exception as e:
        return jsonify({"message": str(e)}), 500