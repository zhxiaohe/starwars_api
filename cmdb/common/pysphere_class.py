import pysphere

from pysphere import VIServer


class pp_pysphere(object):
    def __init__(self, HOST, USER, PASSWORD):
        self.server = self.connect(HOST, USER, PASSWORD)
        self.obj = {
            'Datastore': [
                'summary.capacity',
                'summary.freeSpace',
                'summary.type',
                'summary.name',
            ],
            'HostSystem': [
                'summary.hardware.cpuMhz',
                'summary.hardware.cpuModel',
                'summary.hardware.memorySize',
                'summary.hardware.model',
                'summary.hardware.numCpuCores',
                'summary.hardware.numCpuPkgs',
                'summary.hardware.numCpuThreads',
                'summary.hardware.uuid',
                'summary.hardware.vendor',
                'summary.host',
                'summary.managementServerIp',
                'summary.overallStatus',
                'summary.quickStats.overallMemoryUsage',
                'summary.quickStats.overallCpuUsage',
                'summary.quickStats.uptime',
                'config.network.pnic',
                'capability.maxHostRunningVms',
                'capability.maxRunningVMs',
                'capability.maxSupportedVMs'
            ],
            'VirtualMachine': [
                'summary.vm',
                'summary.config.numEthernetCards',
                'summary.config.annotation',
                'summary.config.numVirtualDisks',
                'summary.quickStats.overallCpuUsage',
                'summary.quickStats.guestMemoryUsage',
                'summary.quickStats.ftLogBandwidth',
                'summary.quickStats.hostMemoryUsage',
                'summary.quickStats.uptimeSeconds',
                'summary.runtime.powerState',
                'summary.runtime.bootTime',
                'summary.runtime.host',
                'summary.runtime.maxCpuUsage',
                'summary.runtime.maxMemoryUsage',
                'summary.storage.committed',
                'summary.storage.uncommitted',
                'summary.storage.unshared',
                'summary.storage.timestamp',
                'guestHeartbeatStatus',
                'guest.toolsStatus',
                'guest.toolsVersionStatus',
                'guest.toolsVersion',
                'guest.guestId',
                'guest.guestFullName',
                'guest.guestState',
                'guest.ipAddress',
                'guest.hostName',
                'name',
                'parent',
                'config.template',
                'config.hardware.numCPU',
                'config.hardware.memoryMB'
            ]
        }

    def connect(self, HOST, USER, PASSWORD):
        server = VIServer()
        server.connect(HOST, USER, PASSWORD)
        return server

    def disconnect(self):
        self.server.disconnect()

    def get_server_type(self):
        return self.server.get_server_type()

    def get_api_version(self):
        return self.server.get_api_version()

    def power_on(self,name):
        vm = self.server.get_vm_by_name(name)
        vm.power_on(sync_run=True)
        return True

    def power_off(self,name):
        vm = self.server.get_vm_by_name(name)
        vm.power_off(sync_run=True)
        return True

    def destroy(self,name):
        vm = self.server.get_vm_by_name(name)
        vm.destroy(sync_run=True)
        return True

    def get_properties(self):
        '''
            Get properties
        '''
        propertieslist = []
        propertiesdict = {}
        server_properties = self.get_server_properties()
        server_stores = self.get_server_stores()
        for i in range(len(server_properties)):
            propertytmp = dict(server_properties[i], **server_stores[i])
            propertieslist.append(propertytmp)
        for i in range(len(propertieslist)):
            propertiesdict[propertieslist[i]['Host_Id']] = propertieslist[i]
        vmware_properties = self.get_vmware_properties()
        properties = dict(propertiesdict, **vmware_properties)
        return properties

    def get_vmware_properties(self):
        '''
            Get Vmware Properties
        '''
        properties = {}
        props = self.server._retrieve_properties_traversal(property_names=self.obj['VirtualMachine'],
                                                           obj_type='VirtualMachine')
        for prop in props:
            mor = prop.Obj
            msg = {}
            for p in prop.PropSet:
                msg[p.Name] = p.Val
            properties[mor] = msg
        return properties

    def get_server_properties(self):
        '''
            Get Server Summary Properties
        '''
        properties = []
        for d, hname in self.server.get_hosts().items():
            props_hostsystem = self.server._retrieve_properties_traversal(property_names=self.obj['HostSystem'],
                                                                          from_node=d, obj_type='HostSystem')
            for prop in props_hostsystem:
                msg = {}
                for p in prop.PropSet:
                    if p.Name == 'config.network.pnic':
                        mac_address = []
                        net_dev_name = []
                        for i in p.Val.__dict__['_PhysicalNic']:
                            mac_address.append(i.__dict__['_mac'])
                            net_dev_name.append(i.__dict__['_device'])
                        msg['Mac_Address'] = ','.join(mac_address)
                        msg['Net_Dev_Name'] = ','.join(net_dev_name)
                    elif p.Name == 'summary.hardware.cpuMhz':
                        msg['Physical_Cpu_Mhz'] = p.Val
                    elif p.Name == 'summary.hardware.cpuModel':
                        msg['Physical_Cpu_Model'] = p.Val
                    elif p.Name == 'summary.hardware.memorySize':
                        msg['Physical_Memory'] = str(p.Val / 1024 / 1024 / 1024) + 'G'
                    elif p.Name == 'summary.hardware.numCpuCores':
                        msg['Physical_Cpu_Cores'] = p.Val
                    elif p.Name == 'summary.hardware.numCpuPkgs':
                        msg['Physical_Cpu_Pkgs'] = p.Val
                    elif p.Name == 'summary.hardware.numCpuThreads':
                        msg['Logical_Cpu_Cores'] = p.Val
                    elif p.Name == 'summary.hardware.uuid':
                        msg['Device_UUID'] = p.Val
                    elif p.Name == 'summary.hardware.vendor':
                        msg['Device_Type'] = p.Val
                    elif p.Name == 'summary.overallStatus':
                        msg['Device_Status'] = p.Val
                    elif p.Name == 'summary.quickStats.uptime':
                        msg['Device_Uptime'] = p.Val
                    elif p.Name == 'capability.maxHostRunningVms':
                        msg['Max_Host_Running_Vms'] = p.Val
                    elif p.Name == 'summary.hardware.model':
                        msg['Device_Model'] = p.Val
                    elif p.Name == 'summary.host':
                        msg['Host_Id'] = p.Val
                        msg['ipAddress'] = self.get_host_list()[p.Val]
                properties.append(msg)
        return properties


    def get_server_stores(self):
        '''
            Get Server Stores Message
        '''
        Datastore = []
        props = self.server._retrieve_properties_traversal(property_names=self.obj['Datastore'], obj_type="Datastore")
        for prop_set in props:
            datastore = {}
            for prop in prop_set.PropSet:
                msg = {}
                if prop.Name == "summary.capacity":
                    datastore['Datastore_Space'] = str(prop.Val / 1073741824) + 'G'
                elif prop.Name == "summary.freeSpace":
                    datastore['DatastoreFreespace'] = str(prop.Val / 1073741824) + 'G'
                elif prop.Name == "summary.name":
                    datastore['Datastore_Name'] = prop.Val
                elif prop.Name == "summary.type":
                    datastore['Datastore_Type'] = prop.Val
                msg[prop.Name] = prop.Val
            Datastore.append(datastore)
        return Datastore

    def get_host_list(self):
        return self.server.get_hosts()
