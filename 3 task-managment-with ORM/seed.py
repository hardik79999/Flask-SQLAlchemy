from app import app   # tera main Flask app file
from models import db, Users
from werkzeug.security import generate_password_hash

def seed_admin():

    with app.app_context():   # 🔥 important for SQLite

        # check if already exists
        existing_admin = Users.query.filter_by(email="admin@test.com").first()
        if existing_admin:
            print("⚠️ Admin already exists")
            return

        # create admin
        admin = Users(
            role="admin",
            username="admin",
            email="admin@test.com",
            password=generate_password_hash("123")
        )

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin created successfully!")


if __name__ == "__main__":
    seed_admin()