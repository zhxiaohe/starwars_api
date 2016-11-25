# -*- coding: utf-8 -*-
from flask import session
from flask.ext.restful import Resource, reqparse, marshal_with

from models import User
from common.util import *
from common.token_manager import Token_Manager
from config import my_response_fields

class Login(Resource):
    '''
        Login
    '''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True, location = 'json')
        self.reqparse.add_argument('password', type = str, required = True, location = 'json')
        super(Login, self).__init__()

    @marshal_with(my_response_fields)
    def post(self):
        args = self.reqparse.parse_args(strict=True)
        username = args.get('username')
        password = args.get('password')

        if not username or not password:
            return my_response(dict(result=False,message='User or Password is None',code=402))

        userobj = User.query.filter_by(username = username).first()

        if not userobj:
            return my_response(dict(result=False,message='User is not exist'))

        if not userobj.verify_password(password):
            return my_response(dict(result=False,message='Password Error'))

        userid = userobj.id

        data = dict(username=username,userid=userid)

        tokencls = Token_Manager()
        token = tokencls.generate_auth_token(data= data)

        rolelist = []
        u = User.query.get(userid)
        r = u.role.all()
        for p in r:
            rolelist.append(p.rolename)

        rolelist = map( lambda x:unicode.encode(x) ,rolelist)

        UUID = get_uuid()

        response_data = dict(uuid=UUID,username=username,userid=userid,role=rolelist)
        redis_data = dict(token=token,username=username,userid=userid)

        tokencls.redis_set(k=UUID,v=redis_data)

        log(level='info', message='Login Sucess,Username=%s' % username)

        return my_response(dict(result=True,message='Login Success',data=response_data))

class Logout(Resource):
    '''
        Logout
    '''
    @marshal_with(my_response_fields)
    def get(self):
        session.clear()

        log(level='info', message='Logout Sucess')
        return my_response(dict(result=True,message='Logout Sucess'))

