from flask import request , jsonify
from models import Blog , db


def read_blog_routs():
    posts = Blog.query.all()

    all_blog = [post.to_dict() for post in posts]

    return jsonify({

            "status": True,
            "message": all_blog
    })