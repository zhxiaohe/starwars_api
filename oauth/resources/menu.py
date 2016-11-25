# -*- coding: utf-8 -*-
from flask.ext.restful import Resource
from common.util import *
from models import User

class Menu(Resource):
    '''
        List menu
    '''
    method_decorators = [ login_required ]
    def get(self):
        usermsg =  parse_session()
        if type(usermsg) == dict:
            userid = usermsg['userid']

        menulist = []
        menupidnozerolist = []
        u = User.query.get(userid)
        r = u.role.all()
        for p in r:
            for j in p.perms:
                if j.pid == 0:
                    menu = dict(id=j.id,menu=j.menu,type=j.type,uri=j.uri,method=j.method,icon=j.icon,pid=j.pid,subMenu=[])
                    menulist.append(menu)
                else:
                    menupidnozerolist.append(j)

        for i in menupidnozerolist:
            menu = dict(id=i.id,menu=i.menu,type=i.type,uri=i.uri,method=i.method,icon=i.icon,pid=i.pid,subMenu=[])
            menumanager(l=menulist,pid=i.pid,menudata=menu)

        log(level='info', message='Get menu list by userid : %s' % userid)

        response = dict(result=True, data=menulist,code='200',message='Sucess')
        return my_response(response)