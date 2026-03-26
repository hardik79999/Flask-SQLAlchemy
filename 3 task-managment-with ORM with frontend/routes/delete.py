from flask import request, jsonify
from models import Users, Tasks, db

def delete_routs(current_user):

    data = request.get_json()

    task_uuid = data.get('uuid')


    if not task_uuid:
        return jsonify({"message": "Task UUID is required"}), 400
    
    try:

        task = Tasks.query.filter_by(uuid=task_uuid).first()

        if not task:
            return jsonify({"message": "Task not found"}), 404

        # MANAGER
        if current_user['role'] == "manager":

            if task.assigned_by != current_user['id']:
                return jsonify({"message": "You can only delete your own employee tasks"}), 403
            
            if task.is_active == False:
                return jsonify({"message": "Tasks not found or already deleted."}), 404


            task.is_active = False
            
        # ADMIN
        elif current_user['role'] == "admin":
            
            if task.is_active == False:
                return jsonify({"message": "Tasks not found or already deleted."}), 404
            
            task.is_active = False

        # EMPLOYEE                    
        else:
            return jsonify({"message": "Employee are not 'delete' tasks...!!!"}), 403
    
        
        db.session.commit()

        return jsonify({
            "message": "Task deleted successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500



