class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5433/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
