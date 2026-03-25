from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)

    blogs = db.relationship('Blog', backref='author', lazy=True)