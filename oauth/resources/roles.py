# -*- coding: utf-8 -*-
from flask import jsonify, request, abort
from flask.ext.restful import Resource, marshal_with,reqparse

from common.util import json_message, dbadd, dbdel, login_required, abort_if_id_doesnt_exist,log,check_perms

from models import User,Role,Perm,Roles_Perms,db


class RolesList(Resource):
    method_decorators = [ login_required , check_perms ]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('rolename', type = str, required = True, location = 'json')
        super(RolesList, self).__init__()

    def get(self):
        '''
            list all roles

        '''
        #try:
        role=Role.query.all()
        rolelist=[{'id': i.id, 'rolename': i.rolename} for i in role]
        return  rolelist

    def post(self):
        """
            add roles
        """
        args = self.reqparse.parse_args(strict=True)
        rolename = args.get('rolename')

        if not rolename:
            return json_message(200, 'error', 'the new rolename is None')
    
        u = Role(rolename=rolename)
        dbadd(u)
        
        log(level='info', message='Create new role: name=%s' % rolename)

        return json_message(200, 'message', 'Roles Register Success')


class Rolesid(Resource):
    method_decorators = [login_required , check_perms]
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('rolename', type = str, required = True, location = 'json')
        super(Rolesid, self).__init__()

    def get(self,roleid):
        '''
            by rolesid get the user roles
        '''
        role=Role.query.filter_by(id=roleid).first() 

        if  role:
            return {'roleid': role.id, 'rolename': role.rolename}
        else:
            return json_message(410, 'error', 'roleid is None')


    def put(self,roleid):
        '''
            update roles
        '''

        abort_if_id_doesnt_exist(Role, id=roleid)

        args = self.reqparse.parse_args(strict=True)

        name = args.get('rolename')

        if not name:
            return json_message(200, 'error', 'the new rolename is None')

        query = db.session.query(Role)

        try:
            query.filter(Role.id == roleid).update( { Role.rolename:name})
            query.session.commit()
        except Exception:
            return json_message(410, 'error', 'Rolename Change Failed')

        log(level='info', message='Update role: name=%s id=%s' % (name,roleid))

        return json_message(200, 'message', 'Rolnename Change Success')


    def delete(self,roleid):
        '''
            delete rolename
        '''
        #prolename=request.form['rolename'] 
        #rolename = request.json.get('rolename', None)


        args = self.reqparse.parse_args(strict=True)

        rolename = args.get('rolename')

        abort_if_id_doesnt_exist(Role,rolename=rolename)

        role=Role.query.filter_by(id=roleid).first()

        if  rolename == role.rolename:
            #dbdel(Role, id=roleid)
            db.session.query(Role).filter_by(id=roleid).delete()
            db.session.commit()
        else:
            return json_message(410, 'error', 'Rolename Change Failed')

        log(level='warning', message='Delete role: name=%s id=%s' % (rolename,roleid))

        return json_message(200, 'message', 'role Delete Success')


class RolesPerm(Resource):
    method_decorators = [login_required , check_perms]

    def get(self,roleid):
        '''
            by rolesid get the user roles
        '''
        r=Role.query.get(roleid)
        if not r:
            return json_message(410, 'error', 'roleid is None')
        perm={}
        num=0
        for i in r.perms:
            perm[num]=i.uri
            num+=1

        return {'role': roleid, 'permname': perm}


    def put(self,roleid):
        '''
            roles add permsid
        '''
        permsid = request.json.get('permid', None)

        return permsid 
        if not permsid:
            return json_message(200, 'error', 'Permsid is None')

        r=Role.query.get(roleid)    

        for id in permsid:
            p=Perm.query.get(id)
            if not p:
                return json_message(200, 'error', 'Permsid is None: id=%s ' % id  )


        if  r:
            for id in permsid:
                r.perms.append(Perm.query.get(id))
            db.session.add(r)               
            db.session.commit()             
        else:
            return json_message(410, 'error', 'None')

        log(level='info', message='Update role vs perm: perm=%s roleid=%s' % (permsid,roleid))
            
        return json_message(200, 'message', 'roleid add permsid  Success')
