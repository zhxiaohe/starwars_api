from werkzeug.exceptions import HTTPException
import os
from flask.ext.restful import fields
import json
basedir = os.path.abspath(os.path.dirname(__file__))

# Mysql Connect Config
MysqlHost = '10.1.15.131'
MysqlUser = 'root'
MysqlPass = 'unfae2016'
MysqlDB = 'ops'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://%s:%s@%s/%s' % (MysqlUser, MysqlPass, MysqlHost, MysqlDB)
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#Redis Configuration
RedisHost = '10.1.15.93'
RedisPost = '6379'

SECRET_KEY = '\xa8H\xe4;R@pi:Mo\x92\xe4M\xa7*E\x80\n\x8d\xfav3\xd8'

TIMEOUT = 3600

# Config Logging ...
from app import app
app.debug = True
import logging
from logging.handlers import RotatingFileHandler
file_handler = RotatingFileHandler('/tmp/flask.log')
file_handler.setLevel(logging.DEBUG)
logging_format = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
)
file_handler.setFormatter(logging_format)
app.logger.addHandler(file_handler)

class UserOrPassIsNone(HTTPException):
    code = 402
    description = 'User or Password is None'

class ToJson(fields.Raw):
    def format(self, value):
        return json.dumps(value)

my_response_fields = {
    'code'      : fields.Integer(default = 200),
    'result'    : fields.Boolean,
    'message'   : fields.String(default= 'Success'),
    'data'      : ToJson(default= 'Null'),
}

ERRORS = {
    'Unauthorized': {
        'message': "Not Authorized.",
        'status': 401,
    },
    'FORBIDDEN': {
        'message': "No Permission.",
        'status': 403,
    },
    'NotFound': {
        'message': "The requested URL was not found on the server.",
        'status': 404,
    },
    'RequestTimeout': {
        'message': "Request Token Timeout.",
        'status': 408,
    },
    'Conflict': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
    'Gone': {
        'data':'Null',
        'message': "ID is not exist.",
        'code': 410,
        'status': 410,
    },
}