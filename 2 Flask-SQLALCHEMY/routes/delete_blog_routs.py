from flask import request , jsonify
from models import Blog , db


def delete_blog_routs(id):

    post = Blog.query.get(id)

    if not post:
        return jsonify({
            "status": "error",
            "message": f"No blog found with id {id}"
        }), 404 
    
    db.session.delete(post)
    db.session.commit()

    return jsonify({
        "status": "delete successfully...",
        "message": post.to_dict()
    }), 200