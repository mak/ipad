import os
import uuid
import idaapi,idc
import ConfigParser
from collections import OrderedDict

class AttrDict(OrderedDict):
    def __getattr__(self,name):
        if name in self:
            return self[name]
        return super(AttrDict,self).__getattr__(name)

class C(object):

    main_cfg = os.path.join(idaapi.get_user_idadir(),'ipad.cfg')
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(C, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    def parse_config(self,c):
        import shutil
        ## this is new analysis
        if not os.path.exists(c):
            shutil.copy(self.main_cfg,c)

            
        self.cfg = ConfigParser.ConfigParser(dict_type=AttrDict)
        self.cfg.read(c)
        ## set shit as attribs
        for s in self.cfg._sections:
            setattr(self,s,self.cfg._sections[s])

    @classmethod
    def filename(cls):
        return os.path.split(idc.GetIdbPath())[-1]

    @classmethod
    def dirname(cls):
        return os.path.join(idaapi.get_user_idadir(),'ipad')
    
class Config(C):


    cfg_file = None

    def __init__(self,*a,**k):
        super(Config,self).__init__(*a,**k)
        self.cfg_file = os.path.join(idaapi.get_user_idadir(),'ipad',C.filename() +'.cfg')

    def __get_default_uid(self):
        self.uid  = str(uuid.uuid4()).replace('-','')
        
    def __get_default_db(self):
        path,_ = os.path.splitext(self.cfg_file)
        path  += '.db'
        self.cfg.set('main','dbpath',path)


    def load_cfg(self):
        if not bool(idc.GetIdbPath()):
            self.cfg_file = self.main_cfg
            
        self.parse_config(self.cfg_file)
        for f in ['user','key','automatic']:
           setattr(self,f,self.main[f])

    def save_file(self):
        with open(self.cfg_file,'w') as f:
            self.cfg.write(f)

    def set_value(self,n,v):
        self.cfg.set('main',n,v)
        self.save_file()

            
    @property
    def db(self):
        if not hasattr(self.main,'dbpath'):
            self.__get_default_db()
        return self.main.dbpath
    
    @property
    def uid(self):
        if not hasattr(self.main,'uid'):
            self.__get_default_uid()
        return self.main.uid
    
    @uid.setter
    def uid(self,v):
        self.set_value('uid',v)
        
    @property
    def ssid(self):
        return int(self.main.ssid)
    
    @ssid.setter
    def ssid(self,v):
        self.set_value('ssid',v)
        
__all__ = [Config]

