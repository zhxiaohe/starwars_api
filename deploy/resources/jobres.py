#coding=utf-8
from flask.ext.restful import Resource
import requests
from config import headers, rundeck_host

class JobRes(Resource):
    def get(self,jobiid):
        url = rundeck_host + '/api/16/execution/' + jobiid + '/state'
        r = requests.get(url,headers=headers)
        return r.text