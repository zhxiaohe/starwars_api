# -*- coding: utf-8 -*-
from flask import jsonify, request, abort
from flask.ext.restful import Resource, marshal_with,reqparse,marshal
from models import db, IDC, vCenter, Asset, Esxi_Server,Vmware,Esxi_Vmware
from common.util import  dbadd, my_response, abort_if_id_doesnt_exist, dbupdate, dbdel, check_perms, login_required
from common.register import Init

from config import my_response_fields


class idcs(Resource):
    #method_decorators = [ check_perms, login_required ]
    method_decorators = [ login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Name', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Address', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Contact', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Phone', type = str, required = True, location = 'json')
        self.reqparse.add_argument('id', type = str, required = False, location = 'json')
        super(idcs, self).__init__()

    #@marshal_with(my_response_fields)
    def get(self):
        '''
        '''
        idc=IDC.query.all()

        idclist=[{ 'id':i.id , 'Name':i.Name  ,'Address':i.Address , 'Contact':i.Contact  , 'Phone':i.Phone } for i in idc]

        da={ "code": 200, "data": idclist, "message": "Success", "result": True }

        return  my_response(da)

    @marshal_with(my_response_fields)
    def post(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        IDCname = args.get('Name')
        Address = args.get('Address')
        Contact = args.get('Contact')
        Phone   = args.get('Phone')
        
        if  IDCname and  Address and  Contact and Phone:
            addidc = IDC(Name=IDCname,Address=Address,Contact=Contact,Phone=Phone)            
            dbadd(addidc)
            '''log'''
            return  my_response(dict(result=True, message='NEW IDC add  Success'))

        else:
            return my_response(dict(result=False,message='ID is not exist', code=410))


    @marshal_with(my_response_fields)
    def put(self):
        '''
        '''

        args = self.reqparse.parse_args(strict=True)

        idcid = args.get('id')
        del args['id']
        
        IDC.query.filter_by(id=idcid).update(args)
        db.session.commit()

        return my_response(dict(result=True, message='IDC update Success'))


    @marshal_with(my_response_fields)
    def delete(self):
        '''
        '''

        parser = reqparse.RequestParser()
        parser.add_argument('id', type = str, required = True, location = 'json')
        args = parser.parse_args()
        idcid = args.get('id')


        idcobj = abort_if_id_doesnt_exist(IDC, id=idcid)
        if not idcobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(IDC, id=idcid)

        #log(level='info', message='Delete User: userid=%s' % userid)

        return my_response(dict(result=True, message='IDC Delete Success'))









class vcenters(Resource):
    #method_decorators = [ check_perms, login_required ]
    method_decorators = [ login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('host', type = str, required = True, location = 'json')
        self.reqparse.add_argument('user', type = str, required = True, location = 'json')
        self.reqparse.add_argument('area', type = str, required = True, location = 'json')
        self.reqparse.add_argument('password', type = str, required = True, location = 'json')
        self.reqparse.add_argument('id', type = str, required = False, location = 'json')
        super(vcenters, self).__init__()

    #@marshal_with(my_response_fields)
    def get(self):
        '''
        '''
        vc=vCenter.query.all()

        idclist=[{ 'id':i.id , 'host':i.host  ,'user':i.user , 'area':i.area   } for i in vc]

        da={ "code": 200, "data": idclist, "message": "Success", "result": True }

        return  my_response(da)


    @marshal_with(my_response_fields)
    def post(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        vc = vCenter(**args)
        dbadd(vc)
        return  my_response(dict(result=True, message='NEW vcenter add  Success'))


    @marshal_with(my_response_fields)
    def put(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        vcid=args.get('id')
        del args['id']

        vCenter.query.filter_by(id=vcid).update(args)
        db.session.commit()

        return my_response(dict(result=True, message='vcenter update Success'))


    @marshal_with(my_response_fields)
    def delete(self):
        '''
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('id', type = str, required = True, location = 'json')
        args = parser.parse_args()
        vcid=args.get('id')

        idcobj = abort_if_id_doesnt_exist(vCenter, id=vcid)
        if not idcobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(vCenter, id=vcid)

        #log(level='info', message='Delete User: userid=%s' % userid)

        return my_response(dict(result=True, message='vcenter Delete Success'))









class assets(Resource):
    #method_decorators = [ check_perms, login_required ]
    method_decorators = [ login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Host_Id', type = str, required = True, location = 'json')            
        self.reqparse.add_argument('System_Hostname', type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Ip', type = str, required = True, location = 'json')          
        self.reqparse.add_argument('Device_type', type = str, required = True, location = 'json')        
        self.reqparse.add_argument('Device_model', type = str, required = True, location = 'json')       
        self.reqparse.add_argument('System_Kernel', type = str, required = True, location = 'json')      
        self.reqparse.add_argument('System_Version', type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Mac', type = str, required = True, location = 'json')         
        self.reqparse.add_argument('Physical_Memory', type = str, required = True, location = 'json')    
        self.reqparse.add_argument('System_Swap', type = str, required = True, location = 'json')        
        self.reqparse.add_argument('Memory_Slots_Number', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Logical_Cpu_Cores', type = str, required = True, location = 'json')  
        self.reqparse.add_argument('Physical_Cpu_Cores', type = str, required = True, location = 'json') 
        self.reqparse.add_argument('Physical_Cpu_Model', type = str, required = True, location = 'json') 
        self.reqparse.add_argument('Hard_Disk', type = str, required = True, location = 'json')          
        self.reqparse.add_argument('Ethernet_Interface', type = str, required = True, location = 'json') 
        self.reqparse.add_argument('Device_Sn', type = str, required = True, location = 'json')          
        self.reqparse.add_argument('System_Network_Card', type = str, required = True, location = 'json')
        super(assets, self).__init__()

    #@marshal_with(my_response_fields)
    def get(self):
        asset=Asset.query.all()
        assetlist=[{  'Host_Id' : i.Host_Id            , 
                    'System_Hostname' : i.System_Hostname    ,
                    'System_Ip' : i.System_Ip          ,
                    'Device_type' : i.Device_type        ,
                    'Device_model' : i.Device_model       ,
                    'System_Kernel' : i.System_Kernel      ,
                    'System_Version' : i.System_Version     ,
                    'System_Mac' : i.System_Mac         ,
                    'Physical_Memory' : i.Physical_Memory    ,
                    'System_Swap' : i.System_Swap        ,
                    'Memory_Slots_Number' : i.Memory_Slots_Number,
                    'Logical_Cpu_Cores' : i.Logical_Cpu_Cores  ,
                    'Physical_Cpu_Cores' : i.Physical_Cpu_Cores ,
                    'Physical_Cpu_Model' : i.Physical_Cpu_Model ,
                    'Hard_Disk' : i.Hard_Disk          ,
                    'Ethernet_Interface' : i.Ethernet_Interface ,
                    'Device_Sn' : i.Device_Sn          ,
                    'System_Network_Card' : i.System_Network_Card,
                    } for i in asset]

        da={ "code": 200, "data": assetlist, "message": "Success", "result": True }

        return  my_response(da)
        #return  my_response(dict(result=True, data=data))
        

    @marshal_with(my_response_fields)
    def post(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        asset = Asset(**args)
        dbadd(addidc)
        return  my_response(dict(result=True, message='NEW IDC add  Success'))
            

    @marshal_with(my_response_fields)
    def put(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        hostid=args.get('Host_Id')

        Asset.query.filter_by(Host_Id=hostid).update(args)
        db.session.commit()

        return my_response(dict(result=True, message='Hard_Disk   update Success'))


    @marshal_with(my_response_fields)
    def delete(self):
        '''
        '''

        args = self.reqparse.parse_args(strict=True)
        hostid=args.get('Host_Id')

        idcobj = abort_if_id_doesnt_exist(Asset, Host_Id=hostid)
        if not idcobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(Asset, Host_Id=hostid)

        #log(level='info', message='Delete User: userid=%s' % userid)

        return my_response(dict(result=True, message='Hard_Disk  Delete Success'))



class esxiserver(Resource):
    #method_decorators = [ check_perms, login_required ]
    method_decorators = [ login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Host_Id', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Mac_Address', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Net_Dev_Name', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Cpu_Mhz', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Cpu_Model', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Memory', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Cpu_Cores', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Cpu_Pkgs', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Logical_Cpu_Cores', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_type', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_uuid', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_Status', type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Ip', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_model', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Datastore_Space', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Datastore_Free_Space', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Datastore_Name', type = str, required = True, location = 'json')
        self.reqparse.add_argument('Datastore_Type', type = str, required = True, location = 'json')
        super(esxilist, self).__init__()

    #@marshal_with(my_response_fields)
    def get(self):
        esxi=Esxi_Server.query.all()
        esxilist=[{  'Host_Id' : i.Host_Id            , 
                    'Mac_Address' : i.Mac_Address         ,
                    'Net_Dev_Name' : i.Net_Dev_Name        ,
                    'Physical_Cpu_Mhz' : i.Physical_Cpu_Mhz    ,
                    'Physical_Cpu_Model' : i.Physical_Cpu_Model  ,
                    'Physical_Memory' : i.Physical_Memory     ,
                    'Physical_Cpu_Cores' : i.Physical_Cpu_Cores  ,
                    'Physical_Cpu_Pkgs' : i.Physical_Cpu_Pkgs   ,
                    'Logical_Cpu_Cores' : i.Logical_Cpu_Cores   ,
                    'Device_type' : i.Device_type         ,
                    'Device_uuid' : i.Device_uuid         ,
                    'Device_Status' : i.Device_Status       ,
                    'System_Ip' : i.System_Ip           ,
                    'Device_model' : i.Device_model        ,
                    'Datastore_Space' : i.Datastore_Space     ,
                    'Datastore_Free_Space' : i.Datastore_Free_Space,
                    'Datastore_Name' : i.Datastore_Name      ,
                    'Datastore_Type' : i.Datastore_Type      ,
                    } for i in esxi]

        da={ "code": 200, "data": esxilist, "message": "Success", "result": True }

        return  my_response(da)
        #return  my_response(dict(result=True, data=esxilist))
        

    @marshal_with(my_response_fields)
    def post(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        esxi = Esxi_Server(**args)
        dbadd(esxi)
        return  my_response(dict(result=True, message='NEW IDC add  Success'))
            

    @marshal_with(my_response_fields)
    def put(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        hostid=args.get('Host_Id')
        
        Esxi_Server.query.filter_by(Host_Id=hostid).update(args)
        db.session.commit()

        return my_response(dict(result=True, message='EXSI_SERVER  update Success'))


    @marshal_with(my_response_fields)
    def delete(self):
        '''
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('Host_Id', type = str, required = True, location = 'json')
        args = parser.parse_args()
        hostid=args.get('Host_Id')

        idcobj = abort_if_id_doesnt_exist(Esxi_Server, Host_Id=hostid)
        if not idcobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(Esxi_Server, Host_Id=hostid)

        #log(level='info', message='Delete User: userid=%s' % userid)

        return my_response(dict(result=True, message='ESXI  Delete Success'))




class vmware(Resource):
    #method_decorators = [ check_perms, login_required ]
    method_decorators = [ login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Host_Id' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Hostname' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Ip' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_type' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_model' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Kernel' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Version' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Mac' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Memory' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Swap' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Memory_Slots_Number' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Logical_Cpu_Cores' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Cpu_Cores' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Physical_Cpu_Model' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Hard_Disk' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Ethernet_Interface' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('Device_Sn' , type = str, required = True, location = 'json')
        self.reqparse.add_argument('System_Network_Card' , type = str, required = True, location = 'json')
        super(vmlist, self).__init__()

    #@marshal_with(my_response_fields)
    def get(self):
        esxi=Vmware.query.all()
        vmlist=[{  'Host_Id' : i.Host_Id            , 
                    'System_Hostname' : i.System_Hostname    ,
                    'System_Ip' : i.System_Ip          ,
                    'Device_type' : i.Device_type        ,
                    'Device_model' : i.Device_model       ,
                    'System_Kernel' : i.System_Kernel      ,
                    'System_Version' : i.System_Version     ,
                    'System_Mac' : i.System_Mac         ,
                    'Physical_Memory' : i.Physical_Memory    ,
                    'System_Swap' : i.System_Swap        ,
                    'Memory_Slots_Number' : i.Memory_Slots_Number,
                    'Logical_Cpu_Cores' : i.Logical_Cpu_Cores  ,
                    'Physical_Cpu_Cores' : i.Physical_Cpu_Cores ,
                    'Physical_Cpu_Model' : i.Physical_Cpu_Model ,
                    'Hard_Disk' : i.Hard_Disk          ,
                    'Ethernet_Interface' : i.Ethernet_Interface ,
                    'Device_Sn' : i.Device_Sn          ,
                    'System_Network_Card' : i.System_Network_Card,
                    } for i in esxi]
                    
        da={ "code": 200, "data": vmlist, "message": "Success", "result": True }

        return  my_response(da)
        #return  my_response(dict(result=True, data=vmlist))
        

    @marshal_with(my_response_fields)
    def post(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        vm = Vmware(**args)
        dbadd(vm)
        return  my_response(dict(result=True, message='NEW VM  add  Success'))



    @marshal_with(my_response_fields)
    def put(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        hostid=args.get('Host_Id')
        
        Vmware.query.filter_by(Host_Id=hostid).update(args)
        db.session.commit()

        return my_response(dict(result=True, message='Vmware  update Success'))


    @marshal_with(my_response_fields)
    def delete(self):
        '''
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('Host_Id', type = str, required = True, location = 'json')
        args = parser.parse_args()
        hostid=args.get('Host_Id')

        idcobj = abort_if_id_doesnt_exist(Vmware, Host_Id=hostid)
        if not idcobj:
            return my_response(dict(result=False,message='ID is not exist', code=410))

        dbdel(Vmware, Host_Id=hostid)

        #log(level='info', message='Delete User: userid=%s' % userid)

        return my_response(dict(result=True, message='Vmware  Delete Success'))




class register(Resource):
    #method_decorators = [ check_perms, login_required ]
    method_decorators = [ login_required ]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type = str, required = True, location = 'json')
        super(register, self).__init__()

    #@marshal_with(my_response_fields)
    def get(self):
        '''
        '''
        a=Esxi_Vmware.query.all()
        x=[{ "Host_Id"              : i.Host_Id ,
            "Father_Id"            : i.Father_Id ,
            "Physical_Cpu_Cores"   : i.Physical_Cpu_Cores ,
            "Hard_Disk"            : i.Hard_Disk ,
            "System_Hostname"      : i.System_Hostname ,
            "System_Uptime"        : i.System_Uptime ,
            "System_Ip"            : i.System_Ip ,
            "Ethernet_Cards"       : i.Ethernet_Cards ,
            "Physical_Memory"      : i.Physical_Memory ,
            "Power_Status"         : i.Power_Status ,
            "Guest_Status"         : i.Guest_Status ,
            "HeartBeatStatus"      : i.HeartBeatStatus ,
            "Show_Name"            : i.Show_Name ,
            "Virtual_Disk_Nums"    : i.Virtual_Disk_Nums ,
            "Tool_Status"          : i.Tool_Status } for i in a]
        return x


        return  my_response(da)

    @marshal_with(my_response_fields)
    def post(self):
        '''
        '''
        args = self.reqparse.parse_args(strict=True)
        vcid = args.get('id')
        a=Init(vcid)
        if a[0]:
            return my_response(dict(result=True, message='Vcenter init Success'))
        else:
            if a[2] == "wantry":
                data = [ i for i in a[1]] 
            else:
                data = [ {i:x} for i,x in a[1].items()]

            return my_response(dict(result=a[0], message='Vcenter init is ERROR',data=data))

