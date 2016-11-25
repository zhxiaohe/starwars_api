from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from resources.users import User_List, Register, User_Manager
from resources.perms import Perms_Put_Or_Delete, Perms_List
from resources.roles import RolesList,Rolesid,RolesPerm
from resources.menu import Menu
from resources.login_or_logout import Login, Logout

api = restful.Api(app, errors=app.config['ERRORS'])

api.add_resource(User_List,     '/userslist',               endpoint = '/userslist')
api.add_resource(User_Manager,  '/users/<int:userid>',      endpoint = '/users/<int:userid>')
api.add_resource(Register,      '/register',                endpoint = '/register')
api.add_resource(Login,         '/login',                   endpoint = '/login')
api.add_resource(Logout,        '/logout',                  endpoint = '/logout')

api.add_resource(Perms_Put_Or_Delete, '/perms/<int:permid>',endpoint = '/perms/<int:permid>')
api.add_resource(Perms_List,    '/perms',                   endpoint = '/perms')

api.add_resource(RolesList,     '/roles',                   endpoint = '/roles')
api.add_resource(Rolesid,       '/roles/<int:roleid>',      endpoint = '/roles/<int:roleid>')


api.add_resource(RolesPerm,     '/roletoperm/<int:roleid>', endpoint = '/roletoperm/<int:roleid>')

api.add_resource(Menu,     '/menu', endpoint = '/menu')