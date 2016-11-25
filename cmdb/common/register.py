from flask import jsonify, request, abort
from models import db,  vCenter, Esxi_Server, Vmware, Esxi_Vmware
from common.util import  dbadd, dbdel

from common.pysphere_class import pp_pysphere

def ip_check(ip):
    q = ip.split('.')
    return len(q) == 4 and len(filter(lambda x: x >= 0 and x <= 255, \
                                      map(int, filter(lambda x: x.isdigit(), q)))) == 4

def Init(id):
    p=vCenter.query.filter_by(id=id).first()
    try:
        pysphere = pp_pysphere(HOST=p.host, USER=p.user, PASSWORD=p.password)
        props = pysphere.get_properties()
        errors = {}
        for k, v in props.items():
            if 'host' in k:
                Host_Id = p.area + '-' + k
                Host_Id_List = [i.Host_Id for i in Esxi_Server.query.all()]
                if Host_Id not in Host_Id_List:
                    try:
                        esxi=Esxi_Server(
                            Host_Id=Host_Id,
                            Mac_Address=v.get('Mac_Address', 'Null'),
                            Net_Dev_Name=v.get('Net_Dev_Name', 'Null'),
                            Physical_Cpu_Mhz=v.get('Physical_Cpu_Mhz', 'Null'),
                            Physical_Cpu_Model=v.get('Physical_Cpu_Model', 'Null'),
                            Physical_Memory=v.get('Physical_Memory', 'Null'),
                            Physical_Cpu_Cores=v.get('Physical_Cpu_Cores', 'Null'),
                            Physical_Cpu_Pkgs=v.get('Physical_Cpu_Pkgs', 'Null'),
                            Logical_Cpu_Cores=v.get('Logical_Cpu_Cores', 'Null'),
                            Device_UUID=v.get('Device_UUID', 'Null'),
                            Device_Type=v.get('Device_Type', 'Null'),
                            Device_Status=v.get('Device_Status', 'Null'),
                            System_Ip=v.get('ipAddress', 'Null'),
                            Device_Model=v.get('Device_Model', 'Null'),
                            Datastore_Space=v.get('Datastore_Space', 'Null'),
                            Datastore_Name=v.get('Datastore_Name', 'Null'),
                            Datastore_Type=v.get('Datastore_Type', 'Null'),
                            Datastore_Free_Space=v.get('DatastoreFreespace', 'Null'),
                        )
                        dbadd(esxi)
                    except Exception, e:
                        #runlog(e, level='error')
                        errors[k] = e
                else:
                    dbdel(Esxi_Server, Host_Id=Host_Id)
                    try:
                        esxi=Esxi_Server(
                            Host_Id=Host_Id,
                            Mac_Address=v.get('Mac_Address', 'Null'),
                            Net_Dev_Name=v.get('Net_Dev_Name', 'Null'),
                            Physical_Cpu_Mhz=v.get('Physical_Cpu_Mhz', 'Null'),
                            Physical_Cpu_Model=v.get('Physical_Cpu_Model', 'Null'),
                            Physical_Memory=v.get('Physical_Memory', 'Null'),
                            Physical_Cpu_Cores=v.get('Physical_Cpu_Cores', 'Null'),
                            Physical_Cpu_Pkgs=v.get('Physical_Cpu_Pkgs', 'Null'),
                            Logical_Cpu_Cores=v.get('Logical_Cpu_Cores', 'Null'),
                            Device_UUID=v.get('Device_UUID', 'Null'),
                            Device_Type=v.get('Device_Type', 'Null'),
                            Device_Status=v.get('Device_Status', 'Null'),
                            System_Ip=v.get('ipAddress', 'Null'),
                            Device_Model=v.get('Device_Model', 'Null'),
                            Datastore_Space=v.get('Datastore_Space', 'Null'),
                            Datastore_Name=v.get('Datastore_Name', 'Null'),
                            Datastore_Type=v.get('Datastore_Type', 'Null'),
                            Datastore_Free_Space=v.get('DatastoreFreespace', 'Null'),
                        )
                        dbadd(esxi)
                    except Exception, e:
                        #runlog(e, level='error')
                        errors[k] = e


            elif 'vm' in k:
                Host_Id = p.area + '-' + k
                Father_Id = p.area + '-' + v['summary.runtime.host']
                System_Ip = v.get('guest.ipAddress', 'Null')
                Hard_Disk = str(v.get('summary.storage.committed', 0) / 1073741824) + 'G'
                Physical_Memory = str(v.get('config.hardware.memoryMB', 0) / 1024) + 'G'
                if System_Ip != 'Null':
                    if not ip_check(System_Ip):
                        System_Ip = 'Null'
                Host_Id_List = [i.Host_Id for i in Esxi_Vmware.query.all()]
                if Host_Id not in Host_Id_List:
                    try:
                        vmw=Esxi_Vmware(
                            Host_Id=Host_Id,
                            Father_Id=Father_Id,
                            Physical_Cpu_Cores=v.get('config.hardware.numCPU', 'Null'),
                            Hard_Disk=Hard_Disk,
                            System_Hostname=v.get('guest.hostName', 'Null'),
                            System_Uptime=v.get('summary.quickStats.uptimeSeconds', 'Null'),
                            System_Ip=System_Ip,
                            Ethernet_Cards=v.get('summary.config.numEthernetCards', 'Null'),
                            Physical_Memory=Physical_Memory,
                            Power_Status=v.get('summary.runtime.powerState', 'Null'),
                            Guest_Status=v.get('guest.guestState', 'Null'),
                            HeartBeatStatus=v.get('guestHeartbeatStatus', 'Null'),
                            Show_Name=v.get('name', 'Null'),
                            Virtual_Disk_Nums=v.get('summary.config.numVirtualDisks', 'Null'),
                            Tool_Status=v.get('guest.toolsStatus', 'Null'),
                        )
                        dbadd(vmw)
                    except Exception, e:
                        #runlog(e, level='error')
                        errors[k] = e
                else:
                    
                    dbdel(Esxi_Vmware, Host_Id=Host_Id)
                    try:
                        vmw=Esxi_Vmware(
                            Host_Id=Host_Id,
                            Father_Id=Father_Id,
                            Physical_Cpu_Cores=v.get('config.hardware.numCPU', 'Null'),
                            Hard_Disk=Hard_Disk,
                            System_Hostname=v.get('guest.hostName', 'Null'),
                            System_Uptime=v.get('summary.quickStats.uptimeSeconds', 'Null'),
                            System_Ip=System_Ip,
                            Ethernet_Cards=v.get('summary.config.numEthernetCards', 'Null'),
                            Physical_Memory=Physical_Memory,
                            Power_Status=v.get('summary.runtime.powerState', 'Null'),
                            Guest_Status=v.get('guest.guestState', 'Null'),
                            HeartBeatStatus=v.get('guestHeartbeatStatus', 'Null'),
                            Show_Name=v.get('name', 'Null'),
                            Virtual_Disk_Nums=v.get('summary.config.numVirtualDisks', 'Null'),
                            Tool_Status=v.get('guest.toolsStatus', 'Null'),
                        )
                        dbadd(vmw)
                    except Exception, e:
                        #runlog(e, level='error')
                        errors[k] = e
        pysphere.disconnect()
        if errors:
            return False,errors,"lantry"
        else:
            return [True]
    except Exception, e :
        #runlog(e, level='error')
        return False,e,"wantry"
