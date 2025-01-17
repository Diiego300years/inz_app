import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.getcwd(), '.env'))

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #
    PER_PAGE = 10
    PAGINATION_CSS_FRAMEWORK = "boostrap3"
    PAGINATION_LINK_SIZE = "sm"
    PAGINATION_SHOW_SINGLE_PAGE = False
    PAGINATION_INCLUDE_FIRST_PAGE_NUMBER = False
    PAGINATION_PREV_REL = "prev"
    PAGINATION_NEXT_REL = "next prefetch"
    PAGINATION_RECORD_NAME = "records"
    PAGINATION_FORMAT_TOTAL = True
    PAGINATION_FORMAT_NUMBER = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_APP=os.environ.get('FLASK_APP')

    #docker update
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    # WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    FLASK_APP=os.environ.get('FLASK_APP')

    MAIL_SERVER = os.environ.get('PROD_MAIL_SERVER')
    MAIL_PORT =  os.environ.get('PROD_MAIL_PORT')
    FLASKY_MAIL_SENDER = os.environ.get("PROD_FLASKY_MAIL_SENDER")
    MAIL_USERNAME =  os.environ.get('PROD_MAIL_USERNAME')
    MAIL_PASSWORD =  os.environ.get('PROD_MAIL_PASSWORD')

    FLASKY_ADMIN =  os.environ.get("PROD_FLASKY_ADMIN")
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URL')

    # COOKIE
    # Only for http not js
    SESSION_COOKIE_HTTPONLY = True

########################################## Docker ###############################################

class DevelopmentConfigWithDocker(Config):
    FLASK_ENV = 'default'
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_APP = os.environ.get('FLASK_APP')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DOCKER_DEV_DATABASE_URL')

class TestingConfigWithDocker(Config):
    FLASK_ENV = 'testing'

    # true for turn off errors handling
    TESTING = True
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    FLASK_APP = os.environ.get('FLASK_APP')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DOCKER_TEST_SQLALCHEMY_DATABASE_URI')



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfigWithDocker,
    'developmentWithDocker': DevelopmentConfigWithDocker,
    'testingConfigWithDocker': TestingConfigWithDocker
}
