from flask.ext.restful import Resource

from common.util import login_required

class DeployManager(Resource):
    method_decorators = [login_required]
    def get(self):
        return 'Auth Token success'