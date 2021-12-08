from datetime import datetime
from database import db

class Season(db.Model):
    __tablename__ = 'season'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    
    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, nullable=True)
    ttl = db.Column(db.String(1024), nullable=True)
    detail = db.Column(db.Text(), nullable=True)
    synopsis = db.Column(db.Text(), nullable=True)
    music = db.Column(db.String(1024), nullable=True)
    link = db.Column(db.String(1024), nullable=True)
    checkcount = db.Column(db.Integer, nullable=True)