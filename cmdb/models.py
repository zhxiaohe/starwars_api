from app import db




class IDC(db.Model):
    __tablename__ = 'cmdb_idc'
    id       =  db.Column(db.Integer, primary_key=True)
    Name     =  db.Column(db.String(50)) 
    Address  =  db.Column(db.String(50))
    Contact  =  db.Column(db.String(30))
    Phone    =  db.Column(db.String(30))


class vCenter(db.Model):
    __tablename__ = 'vmware_vcenter'
    id        =   db.Column(db.Integer, primary_key=True) 
    host      =   db.Column(db.String(15)) 
    user      =   db.Column(db.String(50))
    password  =   db.Column(db.String(30))
    area      =   db.Column(db.String(20))






class Asset(db.Model):
    __tablename__ = 'cmdb_asset_1'
    Host_Id             = db.Column(db.String(10), primary_key=True )
    System_Hostname     = db.Column(db.String(50))
    System_Ip           = db.Column(db.String(256))
    Device_type         = db.Column(db.String(64))
    Device_model        = db.Column(db.String(64))
    System_Kernel       = db.Column(db.String(256))
    System_Version      = db.Column(db.String(256))
    System_Mac          = db.Column(db.String(256))
    Physical_Memory     = db.Column(db.String(64))
    System_Swap         = db.Column(db.String(64))
    Memory_Slots_Number = db.Column(db.String(30))
    Logical_Cpu_Cores   = db.Column(db.String(64))
    Physical_Cpu_Cores  = db.Column(db.String(64))
    Physical_Cpu_Model  = db.Column(db.String(64))
    Hard_Disk           = db.Column(db.String(64))
    Ethernet_Interface  = db.Column(db.String(1000))
    Device_Sn           = db.Column(db.String(164))
    System_Network_Card = db.Column(db.String(164))



class Vmware(db.Model):
    __tablename__ = 'cmdb_vmware'
    Host_Id             = db.Column(db.String(10), primary_key=True )
    System_Hostname     = db.Column(db.String(50))
    System_Ip           = db.Column(db.String(256))
    Device_type         = db.Column(db.String(64))
    Device_model        = db.Column(db.String(64))
    System_Kernel       = db.Column(db.String(256))
    System_Version      = db.Column(db.String(256))
    System_Mac          = db.Column(db.String(256))
    Physical_Memory     = db.Column(db.String(64))
    System_Swap         = db.Column(db.String(64))
    Memory_Slots_Number = db.Column(db.String(30))
    Logical_Cpu_Cores   = db.Column(db.String(64))
    Physical_Cpu_Cores  = db.Column(db.String(64))
    Physical_Cpu_Model  = db.Column(db.String(64))
    Hard_Disk           = db.Column(db.String(64))
    Ethernet_Interface  = db.Column(db.String(1000))
    Device_Sn           = db.Column(db.String(164))
    System_Network_Card = db.Column(db.String(164))





class Esxi_Server(db.Model):
    __tablename__ = 'vmware_esxi_server'
    Host_Id              = db.Column(db.String(30), primary_key=True )
    Mac_Address          = db.Column(db.String(100))
    Net_Dev_Name         = db.Column(db.String(100))
    Physical_Cpu_Mhz     = db.Column(db.String(30))
    Physical_Cpu_Model   = db.Column(db.String(64))
    Physical_Memory      = db.Column(db.String(64))
    Physical_Cpu_Cores   = db.Column(db.String(64))
    Physical_Cpu_Pkgs    = db.Column(db.String(64))
    Logical_Cpu_Cores    = db.Column(db.String(64))
    Device_Type          = db.Column(db.String(64))
    Device_UUID          = db.Column(db.String(64))
    Device_Status        = db.Column(db.String(64))
    System_Ip            = db.Column(db.String(256))
    Device_Model         = db.Column(db.String(100))
    Datastore_Space      = db.Column(db.String(100))
    Datastore_Free_Space = db.Column(db.String(100))
    Datastore_Name       = db.Column(db.String(100))
    Datastore_Type       = db.Column(db.String(100))



class Esxi_Vmware(db.Model):
    __tablename__ = 'vmware_esxi_vmware'
    Host_Id             = db.Column(db.String(30), primary_key=True )
    Physical_Cpu_Cores  = db.Column(db.String(64))
    Hard_Disk           = db.Column(db.String(64))
    System_Hostname     = db.Column(db.String(10))
    System_Uptime       = db.Column(db.String(64))
    System_Ip           = db.Column(db.String(100))
    Ethernet_Cards      = db.Column(db.String(64))
    Physical_Memory     = db.Column(db.String(64))
    Father_Id           = db.Column(db.String(64))
    Power_Status        = db.Column(db.String(64))
    Guest_Status        = db.Column(db.String(64))
    HeartBeatStatus     = db.Column(db.String(64))
    Show_Name           = db.Column(db.String(64))
    Virtual_Disk_Nums   = db.Column(db.String(64))
    Tool_Status         = db.Column(db.String(64))



class User(db.Model):
    __tablename__ = 'users'
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(64))
    password        = db.Column(db.String(120))
    role            = db.relationship('Role', backref='users', lazy='dynamic')


Roles_Perms = db.Table('roles_perms',
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('perm_id', db.Integer, db.ForeignKey('perms.id'))
)


class Role(db.Model):
    __tablename__   = 'roles'
    id              = db.Column(db.Integer, primary_key=True)
    rolename        = db.Column(db.String(64))
    userid          = db.Column(db.Integer, db.ForeignKey('users.id'))
    perms           = db.relationship('Perm', secondary=Roles_Perms, backref='roles')


class Perm(db.Model):
    __tablename__   = 'perms'
    id              = db.Column(db.Integer, primary_key=True)
    menu            = db.Column(db.String(120))
    type            = db.Column(db.Integer)
    uri             = db.Column(db.String(120))
    method          = db.Column(db.String(20))
    icon            = db.Column(db.String(120))
    pid             = db.Column(db.Integer)
