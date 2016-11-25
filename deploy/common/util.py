from functools import wraps
from flask import abort, session, jsonify

from common.token_manager import Token_Manager

def json_message(status=200, msgkey='message',msg = None):
    '''
        Formatting jsonify
    '''
    message = {}
    if msgkey == 'message':
        message = {'status': status, 'message': msg}
    elif msgkey == 'error':
        message = {'status': status, 'error': msg}
    return jsonify(message)

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = session.get('token', None)
        if token is None:
            abort(401)
        token = Token_Manager().verify_auth_token(token=token)
        if token == 401:
            abort(401)
        if token == 408:
            abort(408)
        return func(*args, **kwargs)
    return decorated_function

def abort_if_id_doesnt_exist(object,**kwargs):
    obj = object.query.filter_by(**kwargs).first()
    if obj is None:
        abort(410)
    else:
        return obj