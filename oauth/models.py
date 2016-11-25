from app import db
from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = 'users'
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(64))
    password        = db.Column(db.String(120))
    role            = db.relationship('Role', backref='users', lazy='dynamic')

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)


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
