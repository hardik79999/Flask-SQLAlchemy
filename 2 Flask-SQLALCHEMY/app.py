from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db

from routes.create_blog_routs import create_routs
from routes.read_blog_routs import read_blog_routs
from routes.update_blog_routs import update_blog_routs
from routes.delete_blog_routs import delete_blog_routs


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config) # use all setting from Config class


db.init_app(app) # which app are use
migrate = Migrate(app , db) # make migrate app and db


@app.route('/create-blog', methods = ['POST'])
def create():
    return create_routs()


@app.route('/read-blog', methods = ['GET'])
def read():
    return read_blog_routs()


@app.route('/update-blog/<int:id>', methods = ['POST'])
def update(id):
    return update_blog_routs(id)

@app.route('/delete-blog/<int:id>', methods = ['POST'])
def delete(id):
    return delete_blog_routs(id)

if __name__ == "__main__":
    app.run(debug=True)