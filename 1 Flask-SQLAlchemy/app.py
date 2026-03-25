from flask import Flask
from config import Config
from models import db
from flask_migrate import Migrate
from routes.blog_routes import blog_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app , db)

# Register Blueprint
app.register_blueprint(blog_bp)


if __name__ == "__main__":
    app.run(debug=True)