import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'coasaddsf41fsdfawhjk'

    SQLALCHEMY_TRACK_MODIFCATIONS = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR,'app.db')
