import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'vin!@#$%bebb'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = ''
    FLASKY_ADMIN = ''

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')



config = {
    'development': 'DevelopmentConfig',
    'testing': '',
    'production': '',
    'default': DevelopmentConfig
}