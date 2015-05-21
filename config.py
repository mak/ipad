import idaapi,idc
import os
import uuid

class Config(object):

    cfg_file = os.path.join(idaapi.get_user_idadir(),'ipad.cfg')
    
    def __init__(self):
        self._uid = None
        self._dbpath = None
        self.parse_config()
        
    def parse_config(self):
        pass


    def __get_default_uid(self):
        self._uid  = str(uuid.uuid4()).replace('-','')

    def __get_default_db(self):
        path,_ = os.path.splitext(idc.GetIdbPath())
        self._dbpath = path + '.db'

    
    @property
    def db(self):
        if not self._dbpath:
            self.__get_default_db()
        return self._dbpath

    @property
    def uid(self):
        if not self._uid:
            self.__get_default_uid()
        return self._uid
        
