import os
basedir = os.path.abspath(os.path.dirname(__file__)) # Get path of directory that the Python application is running from

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'appDatabase.db') ## Then join the path
    SQLALCHEMY_TRACK_MODIFICATIONS = False