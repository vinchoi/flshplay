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

    # @classmethod
    # def init_app(cls, app):
    #     Config.init_app(app)
    #
    #     import logging
    #     from logging import FileHandler
    #
    #     logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s %(levelname)s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S',
    #                     filename='log\info1.log',
    #                     filemode='w')
    #
    #     logging.debug('dddddddddd')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Vin123456@@127.0.0.1/flshplay'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging import FileHandler
        file_handler = FileHandler(filename='log/err.log', encoding='utf-8')
        fmter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(fmter)
        file_handler.setLevel(logging.ERROR)
        app.logger.addHandler(file_handler)






config = {
    'development': DevelopmentConfig,
    'testing': '',
    'production': ProductionConfig,
    'default': DevelopmentConfig
}