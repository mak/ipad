import os
import json
import uuid
import config
import datetime

from peewee import *


db = SqliteDatabase(config.DB, threadlocals=True)
R_READ = 1 << 0
R_WRITE= 1 << 1

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = PrimaryKeyField()
    username = CharField(unique=True)
    key = CharField()

    @property
    def sessions(self):
        return Session.select().join(UserSess,on=UserSess.session).where(UserSess.user == self.id)

    def _get_restricted_sessions(self,r):
        return ( Session.select().
                 join(UserSess,on=UserSess.session)
                 .where((UserSess.user == self.id) & (UserSess.rights & r)))
    
    def get_readable(self):
        return self._get_restricted_sessions(R_READ)

    def get_writable(self):
        return self._get_restricted_sessions(R_WRITE)

    def get_session(self,ssid):
        try:
            return ( Session.select().
                     join(UserSess,on=UserSess.session)
                     .where((UserSess.user == self.id) &
                            (UserSess.rights & R_READ) &
                            (Session.ssid == ssid))
            ).get()
        except Exception:
            import traceback
            traceback.print_exc()
            return None

    
class IDB(BaseModel):
    uid   = FixedCharField(max_length=32,unique=True)
    name  = CharField()
    owner = ForeignKeyField(User,related_name='idbs')
    
class Session(BaseModel):
    hash  = FixedCharField(max_length=32)
    ssid  = IntegerField(unique=True)
    idb   = ForeignKeyField(IDB,related_name='sessions')
    tag   = CharField()
    type  = BooleanField() ## idb or binary
    timestamp = DateTimeField(default=datetime.datetime.now)

# class Group(BaseModel):
#     id = PrimaryKeyField()
#     rights  = IntegerField()
#     session = ForeignKeyField(Session,related_name='groups')

#     def get_users(self):
#         return User.select().join(UserGroup,on=UserGroup.user).where(UserGroup.group == self.id)


class UserSess(BaseModel):
    user = ForeignKeyField(User)
    session = ForeignKeyField(Session)
    rights = IntegerField()
    
class Change(BaseModel):
    session   = ForeignKeyField(Session,related_name='changes')
    user      = ForeignKeyField(User,related_name='changes')
    timestamp = DateTimeField(default=datetime.datetime.now)
    data      = CharField()
    hash      = FixedCharField(max_length=64)

def start_db():
    new = False
    if not os.path.exists(config.DB):
        new = True
    
    db.connect()
    if new:
#        print BaseModel.__subclasses__()
        db.create_tables(BaseModel.__subclasses__())
##            User,IDB,Session,UserSess])

def get_my_idbs(u):
    return u.idbs


# def get_available_idbs():
#     groups = Group.select().join(UserGroup,on=


def create_user(u,k):
    User(username=u,key=k).save()

def get_user(u,k):
    try:
        return User.select().where((User.username==u) & (User.key==k)).get()
    except:
        return None

def get_idb(uid):
    try:
        return IDB.select().where(IDB.uid == uid).get()
    except:
        return None

def get_session(ssid):
    try:
        return Session.select().where(Session.ssid== ssid).get()
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None

def store_change(msg):
    ss = get_session(msg['ssid'])
    if not ss:
        return
    print 'session'
    del msg['ssid']

    u  = get_user(msg['user'],msg['key'])
    if not u:
        return
    print 'usser'
    del msg['user'];del msg['key']
    tm = datetime.datetime.fromtimestamp(msg['timestamp']); del msg['timestamp']
    h  = msg['hash']; del msg['hash']
    
    Change(user=u.id,session=ss.id,timestamp=tm,hash=h,data=json.dumps(msg)).save()
    return True
# def get_session_owner(sid):
#     return Ses


def save_idb(typ,h,uid,tag,name,user,ssid):

    ## create idb
    idb = get_idb(uid)
    if not idb:
        idb = IDB(uid=uid,name=name,owner=user.id)
        idb.save()
    
    ss = get_session(ssid)
    if not ss:
        ssid = int('0x'+str(uuid.uuid1()).replace('-','')[:8],16)
        ss  = Session(hash=h,idb=idb.id,tag=tag,ssid=ssid,type=typ)
        ss.save()
        UserSess(user=user.id,session=ss.id,rights=R_READ|R_WRITE).save()
        
    r = False
    for s in user.get_writable():
        if s.ssid == ssid:
            r=True
            
    if not r:
        ## create a new session for un-priv users
        ## with new group and add idb owner
        ssid = int('0x'+str(uuid.uuid1()).replace('-','')[:8],16)
        ss  = Session(hash=h,idb=idb.id,tag=tag,ssid=ssid,type=typ)
        ss.save()

        UserSess(user=user.id,session=ss.id,rights=R_READ|R_WRITE).save()
        UserSess(user=idb.owner.id,session=ss.id,rights=R_READ|R_WRITE).save()
        
        
    ## create session

    return str(ss.ssid)


if __name__ == '__main__':
    start_db()
    create_user('mak','3b3f9223fc0e332fd4146ff2989280f42a8ae19c')
    create_user('test','0416887e373c24295632572bc78536c5e3990c48')
    

