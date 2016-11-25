#coding=utf-8
import requests,json

headers = {'X-Rundeck-Auth-Token': '2EcW3xe0urFLrilqUOGCVYLXSbdByk2e','Accept': 'application/json'}

headers['Content-type']='application/json'
rundeck_host= 'http://10.1.16.26:4440'
url = rundeck_host+'/api/16/project/fengyang/run/command'

data={
    'project':'fengyang',
    'exec':'whoami',
    'filter': 'tags: member-web-1,member-web-2',
    'nodeKeepgoing': False  #执行错误之后是否继续
}


r = requests.post(url, headers=headers,data=json.dumps(data))
print r.status_code
print r.text

