import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=1)

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    '\xd7T\xd3k4G\x05<\xd5\xed\xdbK\x14\xdb\xf6\xa3\xad\x18q\xbd\xc3\xfc\xbbJ'
)

SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'sqlite:///{}'.format(os.path.join(basedir, 'db.sqlite'))
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
