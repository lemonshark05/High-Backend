class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5433/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID="339140115579-73sorcnffv0bmdajkej4mrg4efqu7h4g.apps.googleusercontent.com"  # Replace with your Client ID
    GOOGLE_OAUTH_CLIENT_SECRET="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"  # Replace with your Client Secret