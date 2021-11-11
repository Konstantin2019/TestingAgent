from os import path, environ, getenv, urandom
from dotenv import load_dotenv

dir_path = path.abspath(path.dirname(__file__))
dotenv_path = path.join(path.dirname(__file__), '.env')

if path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class BaseConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

class DevelopmentConfig(BaseConfig):
    SECRET_KEY = getenv('SECRET_KEY')
    ADMIN_LOGIN = getenv('ADMIN_LOGIN')
    ADMIN_PASSWORD = getenv('ADMIN_PASSWORD')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(dir_path, 'app/static/sqlite_db/tasks.db')
    FLASK_ENV = 'development'
    ENV = FLASK_ENV
    DEBUG = True

class ProductionConfig(BaseConfig):
    SECRET_KEY = environ.get('SECRET_KEY')
    ADMIN_LOGIN = environ.get('ADMIN_LOGIN')
    ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    FLASK_ENV = 'production'
    ENV = FLASK_ENV
    DEBUG = False