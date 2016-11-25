# -*- coding: utf-8 -*-
from flask.ext.restful import Resource, reqparse, marshal_with

from models import Perm

from common.util import check_perms, abort_if_id_doesnt_exist, dbdel, dbupdate, log, dbadd, login_required, \
    check_method, check_uri, my_response

from config import my_response_fields

class Perms_Put_Or_Delete(Resource):
    method_decorators = [ check_perms, login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('menu', type = str, required = True, location = 'json', help = '', default = '')
        self.reqparse.add_argument('type', type = str, required = True, location = 'json')
        self.reqparse.add_argument('uri', type = check_uri, required = True, location = 'json')
        self.reqparse.add_argument('method', type = check_method, required = True, location = 'json')
        self.reqparse.add_argument('icon', type = str, required = True, location = 'json')
        self.reqparse.add_argument('pid', type = str, required = True, location = 'json')
        super(Perms_Put_Or_Delete, self).__init__()

    @marshal_with(my_response_fields)
    def put(self, permid):
        '''
            Update Perms
        '''
        permobj = abort_if_id_doesnt_exist(Perm, id=permid)
        if not permobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        args = self.reqparse.parse_args()

        dbupdate(Perm, permid, args)

        log(level='info', message='Update Perm: id=%s' % permid)

        return my_response(dict(result=True,message='Perm update Success'))

    @marshal_with(my_response_fields)
    def delete(self, permid):
        '''
            Delete Perms
        '''
        permobj = abort_if_id_doesnt_exist(Perm, id=permid)
        if not permobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(Perm, id=permid)

        log(level='info', message='Delete Perm: id=%s' % permid)

        return my_response(dict(result=True,message='Perm Delete Success'))

class Perms_List(Resource):
    method_decorators = [check_perms, login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('menu', type = str, required = True, location = 'json', help = '', default = '')
        self.reqparse.add_argument('type', type = str, required = True, location = 'json')
        self.reqparse.add_argument('uri', type = check_uri, required = True, location = 'json')
        self.reqparse.add_argument('method', type = check_method, required = True, location = 'json')
        self.reqparse.add_argument('icon', type = str, required = True, location = 'json')
        self.reqparse.add_argument('pid', type = int, required = True, location = 'json')
        super(Perms_List, self).__init__()

    @marshal_with(my_response_fields)
    def get(self):
        '''
            Get all Perms
        '''
        permslist = [{'id': i.id, 'menu': i.menu, 'type': i.type, 'uri': i.uri, 'method': i.method, 'pid': i.pid} for i in Perm.query.all()]

        log(level='info', message='Get Perms List')

        return my_response(dict(result=True,data=permslist))

    @marshal_with(my_response_fields)
    def post(self):
        '''
            Add Perms
        '''
        args = self.reqparse.parse_args()

        perm = Perm(**args)

        dbadd(perm)

        log(level='info', message='Perms add success')

        return my_response(dict(result=True,message='Perms add success'))
