from flask import request , jsonify
from models import Blog , db
def update_blog_routs(id):

    post = Blog.query.get(id)

    data = request.get_json()

    post.title = data.get('title')
    post.description = data.get('description')

    db.session.commit()

    return jsonify({
        "message": "Blog update successfully..."
    }), 200