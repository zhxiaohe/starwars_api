from flask import Flask
from flask.ext import restful
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from resources.cmdb import  idcs, vcenters, assets, esxiserver, vmware, register

api = restful.Api(app, errors=app.config['ERRORS'])

api.add_resource(idcs, '/cmdb/idcs')

api.add_resource(vcenters, '/cmdb/vcenters')

api.add_resource(assets, '/cmdb/machines')

api.add_resource(esxiserver, '/cmdb/esxiserver')

api.add_resource(vmware, '/cmdb/vmware')

api.add_resource(register, '/cmdb/vcenters/register')
