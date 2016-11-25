#coding=utf-8
from flask.ext.restful import Resource
import requests
from config import headers, rundeck_host

#运行某个project下的job,jobid是job编号,返回信息中有job执行自增长id号
"""
{
"id":91,"href":"http://10.1.16.26:4440/api/16/execution/91",
"permalink":"http://10.1.16.26:4440/project/fengyang/execution/show/91",
"status":"running","project":"fengyang","user":"admin",
"date-started":{"unixtime":1459411704805,"date":"2016-03-31T08:08:24Z"},
"job":{"id":"252a9380-10b5-48ad-b0f5-a1ae2fbdd39f","averageDuration":3338,
"name":"deploy:member-backend","group":"","project":"fengyang","description":"member-backend",
"href":"http://10.1.16.26:4440/api/16/job/252a9380-10b5-48ad-b0f5-a1ae2fbdd39f",
"permalink":"http://10.1.16.26:4440/project/fengyang/job/show/252a9380-10b5-48ad-b0f5-a1ae2fbdd39f"},
"description":"whoami [... 3 steps]","argstring":null
}

"""

class RunningJob(Resource):
    def post(self,jobid):
        url = rundeck_host + '/api/16/job/' + jobid + '/run'
        r = requests.post(url,headers=headers)
        return r.text

