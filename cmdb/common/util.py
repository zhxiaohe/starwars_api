# -*- coding: utf-8 -*-
from functools import wraps
from flask import session, jsonify, request, abort, Response

from app import db, app

from common.token_manager import Token_Manager

from models import User

import uuid

import json


def log(level, message):
    '''
        Logging
    '''
    if level == 'info':
        app.logger.info(message)
    elif level == 'warning':
        app.logger.warning(message)
    else:
        app.logger.debug(message)


def dbadd(object):
    '''
        Insert data into Database
    '''
    db.session.add(object)
    dbcommit()
    return True


def dbdel(models, **kwargs):
    '''
        Detele data from Database
    '''
    for value in kwargs.values():
        if not value:
            return None

    db.session.query(models).filter_by(**kwargs).delete()
    dbcommit()
    return True


def dbupdate(model, id, args):
    '''
        Update db
    '''
    model.query.filter_by(id=id).update(args)
    dbcommit()
    return True


def dbcommit():
    '''
        commit db connect
    '''
    db.session.commit()
    return True


def json_message(status=200, msgkey='message', msg=None):
    '''
        Formatting jsonify
    '''
    message = {}
    if msgkey == 'message':
        message = {'status': status, 'message': msg}
    elif msgkey == 'error':
        message = {'status': status, 'error': msg}
    return jsonify(message)


def parse_session():
    Uuid = request.headers.get('Uuid',None)
    # token = session.get('token', None)
    if not Uuid:
        return False
    else:
        usermsg = Token_Manager().redis_get(k=Uuid)
        if not usermsg:
            return False
        else:
            usermsg = eval(usermsg)    #str to dict
            token = usermsg['token']
            token = Token_Manager().verify_auth_token(token=token)
            return token

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = parse_session()
        if not token:
            return my_response(dict(result=False, message='Not Authorized', code=401, data='not token'),code=401)
        else:
            if token == 401:
                return my_response(dict(result=False, message='Not Authorized', code=401, data=''),code=401)
            if token == 408:
                return my_response(dict(result=False, message='Request Token Timeout', code=408, data=''),code=408)
        return func(*args, **kwargs)

    return decorated_function


def get_user_perms(userid):
    permslist = []
    u = User.query.get(userid)
    r = u.role.all()
    for p in r:
        for j in p.perms:
            permslist.append(j.uri)
    return list(set(permslist))


def check_perms(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        uri = request.endpoint
        token = parse_session()
        if type(token) == dict:
            userid = token['userid']
            permslist = get_user_perms(userid=userid)
            if uri not in permslist:
                return my_response(dict(result=False, message='Permission Denied', code=403, data=''),code=403)
        return func(*args, **kwargs)

    return decorated_function


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Origin, Content-Type, Accept, X-Requested-With, uuid')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response


def abort_if_id_doesnt_exist(object, **kwargs):
    obj = object.query.filter_by(**kwargs).first()
    if obj is None:
        return None
    else:
        return obj


def check_method(value):
    '''
        Check api method
    '''
    if value not in ['GET', 'POST', 'PUT', 'DELETE']:
        raise ValueError("Method is not exist")

    return value


def check_uri(value):
    '''
        Check api uri
    '''
    if '/' not in value:
        raise ValueError("Uri Value Error")

    return value


def my_response(data,code=200):
    '''
        Add headers
    '''
    return data, code


def menumanager(l, pid, menudata):
    for i in l:
        if i['id'] == pid:
            i['subMenu'].append(menudata)
        else:
            menumanager(i['subMenu'],pid,menudata)


def get_uuid():
    return str(uuid.uuid1())
