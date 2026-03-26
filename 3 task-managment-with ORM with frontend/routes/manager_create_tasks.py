from flask import request, jsonify
from models import Users, Tasks , db


def manager_create_tasks_routs(current_user):

    if current_user['role'] != 'manager':
        return jsonify({"message": "You are not an Manager. Access Denied."}), 403
    
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    assigned_to_uuid = data.get('assigned_to')

    if not title or not description or not assigned_to_uuid:
        return jsonify({"message": "Missing required fields"}), 400

    try:

        user = Users.query.filter_by(uuid=assigned_to_uuid).first()

        if not user:
            return jsonify({"message": "Invalid UUID! User not found"}), 404
        
        # manager cannot assign task to admin
        if current_user['role'] == "manager" and user.role == 'admin':
            return jsonify({"message": "Manager cannot assign task to Admin"}), 403
        
        # manager can assign only to users created by him
        if current_user['role'] == "manager" and user.created_by != current_user['id']:
            return jsonify({"message": "You can only assign tasks to your own employee"}), 403

        new_task = Tasks(title=title, description=description, assigned_to=user.id, assigned_by=current_user['id'])

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "status": True,
            "username": user.uuid,
            "message": "Task assigned successfully"
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500