#coding=utf-8
from flask.ext.restful import Resource
import requests
from config import headers, rundeck_host

#获取项目列表
class GetProjectlist(Resource):
    def get(self):
        url = rundeck_host + '/api/16/projects'
        r = requests.get(url,headers=headers)
        return r.text
