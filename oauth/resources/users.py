# -*- coding: utf-8 -*-
from flask.ext.restful import Resource, marshal_with, reqparse

from common.util import dbadd, dbdel, login_required, abort_if_id_doesnt_exist, log, my_response, check_perms
from config import my_response_fields

from passlib.apps import custom_app_context as pwd_context
from models import User
from app import db

class User_Manager(Resource):
    method_decorators = [login_required, check_perms]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('password', type = str, required = True, location = 'json')
        super(User_Manager, self).__init__()

    @marshal_with(my_response_fields)
    def get(self,userid):
        '''
            Get users list
        '''
        userobj = abort_if_id_doesnt_exist(User, id = userid)
        if not userobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        role_list = [ {"roleid":i.id,"rolename":i.rolename} for i in userobj.role.all() ]

        data = {
            'username'  : userobj.username,
            'id'        : userobj.id,
            'rolelist'  : role_list
        }

        log(level='info', message='Get User Message: userid=%s' % userid)

        response = dict(result=True, data=data)

        return my_response(response)

    @marshal_with(my_response_fields)
    def put(self,userid):
        '''
            Update user's password
        '''
        userobj = abort_if_id_doesnt_exist(User, id=userid)
        if not userobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        args = self.reqparse.parse_args(strict=True)
        password = args.get('password')

        if not password:
            return my_response(dict(result=False,message='Password is None'))

        query = db.session.query(User)
        newpasswd = pwd_context.encrypt(password)

        try:
            query.filter(User.id == userid).update({User.password: newpasswd})
        except Exception:
            log(level='warning', message='Update Userpassword Failed,userid=%s' % userid)
            return my_response(dict(result=False, message='Password Change Failed'))

        log(level='info', message='Update Userpassword: userid=%s' % userid)

        return my_response(dict(result=True, message='Password Change Success'))

    @marshal_with(my_response_fields)
    def delete(self,userid):
        '''
            Delete User
        '''
        userobj = abort_if_id_doesnt_exist(User, id=userid)
        if not userobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(User, id=userid)

        log(level='info', message='Delete User: userid=%s' % userid)

        return my_response(dict(result=True, message='User Delete Success'))

class User_List(Resource):
    method_decorators = [login_required, check_perms]
    @marshal_with(my_response_fields)
    def get(self):
        '''
            Get users list
        '''
        userslist = [{'id': i.id, 'username': unicode.encode(i.username , "utf-8")} for i in User.query.all()]

        log(level='info', message='Get User List')

        return my_response(dict(result=True, data=userslist))

class Register(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True, location = 'json')
        self.reqparse.add_argument('password', type = str, required = True, location = 'json')
        super(Register, self).__init__()

    @marshal_with(my_response_fields)
    def post(self):
        '''
            User Register
        '''

        args = self.reqparse.parse_args(strict=True)
        username = args.get('username')
        password = args.get('password')

        if not username or not password:
            return my_response(dict(result=False,message='User or Password is None',code=402))

        if User.query.filter_by(username=username).first() is not None:
            return my_response(dict(result=False, message='A user with that username already exists',code=409))

        userobj = User(username=username)
        userobj.hash_password(password)
        dbadd(userobj)

        log(level='info', message='Register Sucess: username=%s' % username)

        return my_response(dict(result=True, message='User Register Success'))
