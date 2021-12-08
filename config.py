import os
class DevelopmentConfig:
    # Flask
    DEBUG = True
    JSON_AS_ASCII = False
    
    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///api.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


Config = DevelopmentConfig