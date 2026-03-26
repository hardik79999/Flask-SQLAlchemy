from flask import request, jsonify
from models import Tasks, Users , db

def update_routs(current_user):

    data = request.get_json()

    new_title = data.get('title')
    new_description = data.get('description')
    new_status = data.get('status')
    task_uuid = data.get('uuid')


    if not task_uuid:
        return jsonify({"message": "Task UUID is required"}), 400
    

    if not new_status and not new_title and not new_description:
        return jsonify({"message": "Please provide at least one field to update"}), 400


    try:
        task = Tasks.query.filter_by(uuid=task_uuid).first()
        
        if not task:
            return jsonify({"message": "Task not found"}), 404



        # EMPLOYEE FIRST
        if current_user['role'] == "employee":
            
            if task.assigned_to != current_user['id']:
                return jsonify({"message": "You can only update your own tasks"}), 403

            if new_title or new_description:
                return jsonify({"message": "Employees can only update status"}), 403

            if new_status:
                valid_statuses = ['pending', 'in progress', 'completed']
                
                if new_status not in valid_statuses:
                    return jsonify({"message": f"Invalid status. Choose from: {valid_statuses}"}), 400
                task.status = new_status
                
            else:
                return jsonify({"message": "Employees can only update the status field"}), 403
            



        # MANAGER
        elif current_user['role'] == "manager":
            if task.assigned_by != current_user['id']:
                return jsonify({"message": "You can only update your own employee"}), 403

            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_status:
                task.status = new_status




        # ADMIN
        elif current_user['role'] == "admin":
            if new_title:
                task.title = new_title
            if new_description:
                task.description = new_description
            if new_status:
                task.status = new_status

        db.session.commit()

        return jsonify({
            "username": current_user['username'],
            "message": "Task updated successfully!"
        }), 200
    


    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500