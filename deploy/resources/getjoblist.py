#coding=utf-8
from flask.ext.restful import Resource
import requests
from config import headers, rundeck_host


#获取某个项目下的job列表
class GetJoblist(Resource):
    def get(self,projectname):
        url = rundeck_host+ '/api/16/project/' + projectname + '/jobs'
        r = requests.get(url,headers=headers)
        return r.text