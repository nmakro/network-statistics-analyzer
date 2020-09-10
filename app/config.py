import os

basedir = os.path.abspath(os.path.dirname(__file__))

DBNAME = "test"


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "mysql+mysqldb://" + "root:rootdb@localhost/" + DBNAME
