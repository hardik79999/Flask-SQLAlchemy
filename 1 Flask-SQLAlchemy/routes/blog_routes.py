from flask import Blueprint, render_template, request, redirect
from models import db, Blog

blog_bp  = Blueprint('blog', __name__)

# READ (All posts)
@blog_bp .route("/")
def index():
    posts = Blog.query.all()
    return render_template("index.html", posts=posts)

# CREATE
@blog_bp .route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        new_post = Blog(name=name, email=email)
        db.session.add(new_post)
        db.session.commit()

        return redirect("/")

    return render_template("create.html")

# UPDATE
@blog_bp .route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = Blog.query.get(id)

    if request.method == "POST":
        post.name = request.form['name']
        post.email = request.form['email']

        db.session.commit()
        return redirect("/")

    return render_template("edit.html", post=post)

# DELETE
@blog_bp .route("/delete/<int:id>")
def delete(id):
    post = Blog.query.get(id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/")