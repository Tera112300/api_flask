from flask_sqlalchemy import SQLAlchemy
# from database import init_db

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)