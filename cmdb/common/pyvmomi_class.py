"""
Written by tanzhixu
Email: tanzhixu@unfae.com
QQ:785925324
"""
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect


class pp_pyvmomi(object):
    def __init__(self, HOST, USER, PASSWORD):
        self.server = self.__connect(HOST, USER, PASSWORD)

    def __connect(self, HOST, USER, PASSWORD):
        try:
            server = SmartConnect(host=HOST, user=USER, pwd=PASSWORD, port=443)
        except IOError, e:
            pass
        return server

    def __template_vm(self, templatename):
        return self.__get_vm_by_name(self.server, templatename)


    def __vmconf(self):
        '''
            CPU/Mem
            mem = 512 #M
            vim.vm.ConfigSpec(numCPUs=1, memoryMB=mem)
        '''
        vmconf = vim.vm.ConfigSpec()
        return vmconf

    def __networkconf(self, ip, subnetmask, gateway):
        '''
            Network setting
        '''
        adaptermap = vim.vm.customization.AdapterMapping()
        adaptermap.adapter = vim.vm.customization.IPSettings(ip=vim.vm.customization.FixedIp(ipAddress=ip),
                                                             subnetMask=subnetmask, gateway=gateway)
        return adaptermap

    def __dns(self, dnslist):
        '''
            dnslist = ['10.1.10.14', '10.1.10.15']
        '''
        return vim.vm.customization.GlobalIPSettings(dnsServerList=dnslist)


    def __hostname(self,domain, hostname):
        '''
            hostname setting
        '''
        return vim.vm.customization.LinuxPrep(domain=domain,
                                              hostName=vim.vm.customization.FixedName(name=hostname))

    def __customspec(self, adaptermap, globalip, identity):
        customspec = vim.vm.customization.Specification(nicSettingMap=[adaptermap], globalIPSettings=globalip,
                                                        identity=identity)
        return customspec

    def __cloneSpec(self, customspec, vmconf):
        '''
            Creating relocate spec and clone spec
        '''
        resource_pool = self.__get_resource_pool(self.server, 'DEV')
        relocateSpec = vim.vm.RelocateSpec(pool=resource_pool)
        cloneSpec = vim.vm.CloneSpec(powerOn=True, template=False, location=relocateSpec, customization=customspec,
                                     config=vmconf)
        return cloneSpec

    def __get_obj(self, content, vimtype, name):
        '''
            Get the vsphere object associated with a given text name
        '''
        obj = None
        container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
        for c in container.view:
            if c.name == name:
                obj = c
                break
        return obj

    def __get_vm_by_name(self, server, name):
        '''
            Find a virtual machine by it's name and return it
        '''
        return self.__get_obj(server.RetrieveContent(), [vim.VirtualMachine], name)

    def __get_resource_pool(self, server, name):
        '''
        Find a virtual machine by it's name and return it
        '''
        return self.__get_obj(server.RetrieveContent(), [vim.ResourcePool], name)

    def __disconnect(self):
        Disconnect(self.server)


    def clone(self, newvm, templatename, vmip, vmsubmask, vmgateway, dnslist, domain, hostname):
        adaptermap = self.__networkconf(ip=vmip, subnetmask=vmsubmask, gateway=vmgateway)
        identity = self.__hostname(domain=domain, hostname=hostname)
        dnslist = self.__dns(dnslist=dnslist)
        customspec = self.__customspec(adaptermap=adaptermap, globalip=dnslist, identity=identity)
        vmconf = self.__vmconf()
        cloneSpec = self.__cloneSpec(customspec=customspec, vmconf=vmconf)
        template_vm = self.__template_vm(templatename=templatename)
        try:
            clone = template_vm.Clone(name=newvm, folder=template_vm.parent, spec=cloneSpec)
        except:
            clone = False
        if clone:
            return True
