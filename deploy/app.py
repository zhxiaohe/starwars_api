from flask import Flask
from flask.ext.restful import  Api
from resources.getprojectlist import GetProjectlist
from resources.getjoblist import GetJoblist
from resources.runningjob import RunningJob
from resources.jobres import JobRes

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)

api.add_resource(GetProjectlist, '/projects')
api.add_resource(GetJoblist, '/project/<string:projectname>')
api.add_resource(RunningJob, '/job/<string:jobid>')
api.add_resource(JobRes, '/job/<string:jobiid>')
