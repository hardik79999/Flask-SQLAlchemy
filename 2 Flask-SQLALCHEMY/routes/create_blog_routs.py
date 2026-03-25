from flask import request, jsonify
from models import Blog , db


def create_routs():
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')

    new_post = Blog(title=title , description=description)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"status": True,
                    "message": "create bolg successfully..."
                    }), 201