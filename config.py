# flake8: noqa
import os
from dotenv import load_dotenv, dotenv_values


PROJECTNAME = 'transporte_sp'
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)
SECRET_KEY = '00110100 00110010'
SESSION_TYPE = 'filesystem'

__version__ = '1.0.0'
__doc__ = "WebApp para avaliação de transportes"

load_dotenv(os.path.join(BASEDIR, '.env'))

# SQLAlchemy settings
# Database configuration
DATABASE_URL = os.environ.get('SQLALCHEMY_DATABASE_URI',
                              dotenv_values().get('SQLALCHEMY_DATABASE_URI',
                                                  'sqlite:///%s/transporte_sp.db' % TOP_LEVEL_DIR))
DEBUG = os.environ.get('FLASK_DEBUG', dotenv_values().get('FLASK_DEBUG'))


class Config:
    """ BASE config """
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_BINDS = {
        'transporte_sp': DATABASE_URL
    }
    SECRET_KEY = os.environ.get('SECRET_KEY', dotenv_values().get('SECRET_KEY')) or SECRET_KEY
    SESSION_TYPE = os.environ.get('SESSION_TYPE', dotenv_values().get('SESSION_TYPE')) or SESSION_TYPE
    BASEDIR = BASEDIR
    TOP_LEVEL_DIR = TOP_LEVEL_DIR
    PROJECTNAME = PROJECTNAME
    DEBUG = DEBUG  # Do not use debug mode in production
    FLASK_DEBUG = DEBUG
