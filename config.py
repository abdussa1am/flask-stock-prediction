import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False  
    #app.config['MAIL_SERVER']='smtp.gmail.com'
    #app.config['MAIL_PORT'] = 465
    #app.config['MAIL_USERNAME'] = 'abdussalam11051998@gmail.com'
    #app.config['MAIL_PASSWORD'] = 'karachiking11051998'
    #app.config['MAIL_USE_TLS'] = False
    #app.config['MAIL_USE_SSL'] = True

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True